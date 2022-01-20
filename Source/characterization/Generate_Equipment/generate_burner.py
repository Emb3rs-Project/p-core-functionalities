"""
alisboa/jmcunha


##############################
INFO: Create Direct Burner Object and characterize its streams.


##############################
INPUT: object with:

        # id - equipment id
        # supply_temperature  [ºC]
        # global_conversion_efficiency
        # fuel_type -  fuel type (natural_gas, fuel_oil, biomass, electricity)
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]
        # excess_heat_supply_temperature
        # excess_heat_flowrate
        # excess_heat_target_temperature

        !!!
        IMPORTANT
        To compute excess heat characteristics the equipment supply capacity must be known.
        The user may choose to add directly the equipment supply_capacity or link processes with the equipment.
            # supply_capacity [kW]
            # processes - vector with processes [process_1,process_2,..]; each process contains dictionary with dictionaries of streams;

                Where, e.g, in process_1:
                    # process_1 = {'streams':[{stream_1_info},{stream_2_info},..]


##############################
OUTPUT: object Burner.

        !!!
        IMPORTANT:
         # burner.streams important attribute for source simulation - Heat Recovery and Convert

"""

from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion import combustion_mass_flows, burner_chamber_temperature
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.fluid_material import fluid_material_cp


class Burner():

    def __init__(self, in_var):

        # Defined Vars
        self.object_type = 'equipment'
        self.equipment_sub_type = 'burner'  # burner
        self.streams = []
        supply_fluid = 'flue_gas'  # Excess heat fluid type
        inflow_fluid = 'air'
        inflow_supply_temperature = 20  # ambient temperature

        # INPUT
        self.id = in_var.id  # Create ID

        try:
            self.global_conversion_efficiency = in_var.global_conversion_efficiency
        except:
            self.global_conversion_efficiency = 0.95

        self.fuel_type = in_var.fuel_type  # Fuel type  (Natural gas, Fuel oil, Biomass)
        excess_heat_supply_temperature = in_var.excess_heat_supply_temperature
        excess_heat_flowrate = in_var.excess_heat_flowrate

        try:
            excess_heat_target_temperature = in_var.excess_heat_target_temperature
        except:
            excess_heat_target_temperature = 120

        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var.daily_periods  # e.g: [[8,12],[15,19]]

        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # get supply capacity to compute excess heat characteristics
        try:
            supply_capacity = in_var.supply_capacity
            self.supply_capacity = supply_capacity
        except:
            processes = in_var.processes
            total_yearly_supply_capacity = 0

            if processes != []:
                for process in processes:
                    for stream in process['streams']:
                        if stream['stream_type'] != 'outflow':
                            total_yearly_supply_capacity += stream.capacity * sum(stream.schedule)

                self.supply_capacity = total_yearly_supply_capacity / (sum(schedule))
            else:
                self.supply_capacity = 0

        # fuel consumption [kg/h]
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        # Inflow
        inflow_flowrate = m_air

        try:
            inflow_target_temperature = in_var.supply_temperature
        except:
            inflow_target_temperature = burner_chamber_temperature(self.fuel_type,
                                                                   fuel_consumption,
                                                                   m_flue_gas)

        inflow_fluid_cp = fluid_material_cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (
                    inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp / 3600  # [kW]

        # equipment streams
        # Air Inflow
        self.streams.append(stream_industry(self.id,
                                            'inflow',
                                            inflow_fluid,
                                            inflow_supply_temperature,
                                            inflow_target_temperature,
                                            inflow_flowrate,
                                            inflow_capacity,
                                            schedule))


        # Excess Heat
        flue_gas_cp = fluid_material_cp(supply_fluid, excess_heat_supply_temperature)
        excess_heat_supply_capacity = excess_heat_flowrate * abs(
                excess_heat_supply_temperature - excess_heat_target_temperature) * flue_gas_cp

        self.streams.append(stream_industry(self.id,
                                            'excess_heat',
                                            supply_fluid,
                                            excess_heat_supply_temperature,
                                            excess_heat_target_temperature,
                                            excess_heat_flowrate,
                                            excess_heat_supply_capacity,
                                            schedule))
