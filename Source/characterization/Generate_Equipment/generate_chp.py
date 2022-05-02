"""
alisboa/jmcunha


##############################
INFO: Create CHP Object and characterize its streams.


##############################
INPUT: object with:

        # id - equipment id
        # supply_temperature [ºC]
        # return_temperature [ºC]
        # global_conversion_efficiency
        # fuel_type -  fuel type (natural_gas, fuel_oil, biomass, electricity)
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]

        !!!
        IMPORTANT
        1) user can input electrical generation or supply heat capacity, with corresponding conversion efficiencies
                # thermal_conversion_efficiency (0 to 1) and supply_capacity [kW]
                # electrical_conversion_efficiency (0 to 1) and electrical_generation [kW]


        2) To compute excess heat characteristics the equipment supply capacity must be known.
        The user may choose to add directly the equipment supply_capacity or link processes with the equipment.
            # supply_capacity [kW]
            # processes - vector with processes [process_1,process_2,..]; each process contains dictionary with dictionaries of streams;

                Where, e.g, in process_1:
                    # process_1 = {'streams':[{stream_1_info},{stream_2_info},..]


##############################
OUTPUT: object CHP.

        !!!
        IMPORTANT:
         # chp.streams important attribute for source simulation - Heat Recovery and Convert

"""

from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion import compute_flue_gas_temperature, combustion_mass_flows
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....utilities.kb import KB


class Chp:

    def __init__(self, in_var, kb: KB):

        ############################################################################################
        # KB
        medium = Medium(kb)

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        inflow_supply_temperature = 20  # Ambient Temperature [ºC]
        inflow_fluid = 'air'

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.fuel_type = in_var['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.equipment_sub_type = 'chp'
        self.supply_capacity = in_var['supply_capacity']
        self.electrical_generation = in_var['electrical_generation']
        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        self.thermal_conversion_efficiency = in_var['thermal_conversion_efficiency']
        self.electrical_conversion_efficiency = in_var['electrical_conversion_efficiency']
        processes = in_var['processes']
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

        ############################################################################################
        # COMPUTE
        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # efficiency
        if self.thermal_conversion_efficiency is None:
            self.thermal_conversion_efficiency = self.global_conversion_efficiency - self.electrical_conversion_efficiency
        elif self.electrical_conversion_efficiency is None:
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.thermal_conversion_efficiency

        # supply capacity
        if self.supply_capacity is None:
            if self.electrical_generation is not None:
                self.supply_capacity = self.electrical_generation / self.electrical_conversion_efficiency * self.thermal_conversion_efficiency  # [kW]
            else:
                self.total_yearly_supply_capacity = 0
                for process in processes:
                    for stream in process['streams']:
                        if stream['stream_type'] != 'outflow':
                            self.total_yearly_supply_capacity += stream['capacity'] * sum(stream['schedule'])
                self.supply_capacity = self.total_yearly_supply_capacity / (sum(schedule))

        # fuel
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb,
                                                                    self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        # excess heat stream
        excess_heat_supply_temperature, inflow_target_temperature = compute_flue_gas_temperature(kb,
                                                                                                 self.supply_capacity,
                                                                                                 self.fuel_type,
                                                                                                 fuel_consumption,
                                                                                                 m_flue_gas)
        # inflow stream
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (
                inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp / 3600  # [kW]

        # GET STREAMS
        # inflow
        self.streams.append(stream_industry(self.id,
                                            'inflow',
                                            inflow_fluid,
                                            inflow_supply_temperature,
                                            inflow_target_temperature,
                                            inflow_flowrate,
                                            inflow_capacity,
                                            schedule))
