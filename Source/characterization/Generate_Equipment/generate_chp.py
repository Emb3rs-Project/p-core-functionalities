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


class Chp():

    def __init__(self, in_var,kb : KB):


        ############################################################################################
        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        inflow_supply_temperature = 20  # Ambient Temperature [ºC]
        inflow_fluid = 'air'
        medium = Medium(kb)


        ############################################################################################
        # INPUT
        self.id = in_var['platform']['id']  # equipment ID
        self.fuel_type = in_var['platform']['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)
        saturday_on = in_var['platform']['saturday_on']
        sunday_on = in_var['platform']['sunday_on']
        shutdown_periods = in_var['platform']['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['platform']['daily_periods']  # e.g: [[8,12],[15,19]]
        self.equipment_sub_type = in_var['platform']['equipment_sub_type']

        try:
            self.global_conversion_efficiency = in_var['platform']['global_conversion_efficiency']
            self.thermal_conversion_efficiency = in_var['platform']['thermal_conversion_efficiency']
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.thermal_conversion_efficiency
        except:
            self.global_conversion_efficiency = in_var['platform']['global_conversion_efficiency']
            self.electrical_conversion_efficiency = in_var['platform']['electrical_conversion_efficiency']
            self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.electrical_conversion_efficiency

        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        try:
            try:
                self.supply_capacity = in_var['platform']['supply_capacity']  # heat [kW]
                self.electrical_generation = self.supply_capacity / self.thermal_conversion_efficiency * self.electrical_conversion_efficiency  # [kW]
            except:
                self.electrical_generation = in_var['platform']['electrical_generation']  # electrical [kW]
                self.supply_capacity = self.electrical_generation / self.electrical_conversion_efficiency * self.thermal_conversion_efficiency  # [kW]

        except:
            try:
                self.supply_capacity = in_var['platform']['supply_capacity']
            except:
                processes = in_var['platform']['processes']
                total_yearly_supply_capacity = 0
                if processes != []:
                    for process in processes:
                        for stream in process['streams']:
                            if stream['stream_type'] != 'outflow':
                                total_yearly_supply_capacity += stream['capacity'] * sum(stream['schedule'])
                    self.supply_capacity = total_yearly_supply_capacity / (sum(schedule))
                else:
                    self.supply_capacity = 0

        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb, self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)
        thermal_capacity = self.electrical_generation / self.electrical_conversion_efficiency

        excess_heat_supply_temperature, inflow_target_temperature = compute_flue_gas_temperature(kb, self.supply_capacity,
                                                                                                 self.fuel_type,
                                                                                                 fuel_consumption,
                                                                                                 m_flue_gas)
        # Inflow ----
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (
                    inflow_target_temperature - inflow_supply_temperature) * inflow_fluid_cp / 3600  # [kW]


        # Get Streams
        self.streams.append(stream_industry(self.id,
                                            'inflow',
                                            inflow_fluid,
                                            inflow_supply_temperature,
                                            inflow_target_temperature,
                                            inflow_flowrate,
                                            inflow_capacity,
                                            schedule))


