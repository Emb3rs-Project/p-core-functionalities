"""
alisboa/jmcunha


##############################
INFO: Create Boiler Object and characterize its streams.


##############################
INPUT: object with:
        # id - equipment ID
        # supply_temperature [ºC]
        # open_closed_loop - 1 (yes)  or 0 (no)
            # if open_closed_loop = 1 -> user must input -> return_temperature [ºC]
        # global_conversion_efficiency  []
        # fuel_type -  fuel type (natural_gas, fuel_oil, biomass, electricity)
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]

        !!!
        IMPORTANT
        To compute excess heat characteristics the equipment supply capacity must be known.
        The user may choose to add directly the equipment supply_capacity or link processes with the equipment.
            # supply_capacity [kW]
            # processes - vector with processes [process_1,process_2,..]; each process contains dictionary with dictionaries of streams;

                Where, e.g, in process_1:
                    # process_1 = {'streams':[{stream_1_info},{stream_2_info},..]


##############################
OUTPUT: object Boiler.

        !!!
        IMPORTANT:
         # boiler.streams important attribute for source simulation - Heat Recovery and Convert

"""

from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.combustion_mass_flows import combustion_mass_flows
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.stream_industry import stream_industry
from ....KB_General.medium import Medium
from ....KB_General.equipment_details import EquipmentDetails
from ....utilities.kb import KB


class Boiler:

    def __init__(self, in_var, kb: KB):

        ############################################################################################
        # KB
        medium = Medium(kb)
        equipment_details = EquipmentDetails(kb)

        # Defined Vars
        self.object_type = 'equipment'
        self.streams = []
        inflow_fluid = 'air'
        inflow_supply_temperature = 20  # Ambient Temperature
        excess_heat_fluid = 'flue_gas'  # Excess heat fluid type
        excess_heat_target_temperature = 120  # flue_gas is usually cooled until 120ºC  due to the formation of condensates

        ############################################################################################
        # INPUT
        self.id = in_var['id']  # equipment ID
        self.fuel_type = in_var['fuel_type']  # Fuel type  (Natural gas, Fuel oil, Biomass)
        self.supply_capacity = in_var['supply_capacity']
        self.global_conversion_efficiency = in_var['global_conversion_efficiency']
        processes = in_var['processes']
        supply_temperature = in_var['equipment_supply_temperature']
        open_closed_loop = in_var['open_closed_loop']  # Open heating circuit? (1-Yes, 0-No)
        saturday_on = in_var['saturday_on']
        sunday_on = in_var['sunday_on']
        shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]

        if open_closed_loop == 1:
            return_temperature = 20  # Ambient Temperature
        else:
            return_temperature = in_var['equipment_return_temperature']

        ############################################################################################
        # COMPUTE
        # schedule
        schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)

        # supply temperature
        if supply_temperature > 100:
            self.equipment_sub_type = 'steam_boiler'
            supply_fluid = 'steam'
        else:
            self.equipment_sub_type = 'hot_water_boiler'
            supply_fluid = 'water'

        # supply capacity
        if self.supply_capacity is None:
            self.total_yearly_supply_capacity = 0
            for process in processes:
                for stream in process['streams']:
                    if stream['stream_type'] != 'outflow':
                        self.total_yearly_supply_capacity += stream['capacity'] * sum(stream['schedule'])

            self.supply_capacity = self.total_yearly_supply_capacity / (sum(schedule))

        # efficiency
        if self.global_conversion_efficiency is None:
            self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(
                self.equipment_sub_type, self.supply_capacity)

        # fuel consumption
        refinement_efficiency = 0.03  # comparing real data and estimate
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(kb,
                                                                    self.supply_capacity,
                                                                    self.global_conversion_efficiency,
                                                                    self.fuel_type)

        # supply heat stream
        supply_flowrate = compute_flow_rate(kb,
                                            supply_fluid,
                                            self.supply_capacity,
                                            supply_temperature,
                                            return_temperature)

        thermal_capacity = self.supply_capacity / self.global_conversion_efficiency

        # excess heat stream
        excess_heat_supply_capacity = thermal_capacity - self.supply_capacity
        excess_heat_flowrate = m_flue_gas

        excess_heat_supply_temperature = excess_heat_target_temperature + excess_heat_supply_capacity/(m_flue_gas/3600*1.4)


        ############################################################
        ############################################################
        ############################################################

        # inflow stream
        inflow_target_temperature = 80
        inflow_flowrate = m_air
        inflow_fluid_cp = medium.cp(inflow_fluid, (inflow_supply_temperature + inflow_target_temperature) / 2)
        inflow_capacity = inflow_flowrate * (inflow_target_temperature - inflow_supply_temperature) \
                          * inflow_fluid_cp / 3600  # [kW]

        # GET STREAMS
        # air inflow
        self.streams.append(stream_industry(self.id,
                                            'inflow',
                                            inflow_fluid,
                                            inflow_supply_temperature,
                                            inflow_target_temperature,
                                            inflow_flowrate,
                                            inflow_capacity,
                                            schedule))

        # supply heat
        self.streams.append(stream_industry(self.id,
                                            'supply_heat',
                                            supply_fluid,
                                            return_temperature,
                                            supply_temperature,
                                            supply_flowrate,
                                            self.supply_capacity,
                                            schedule))

        # excess heat
        self.streams.append(stream_industry(self.id,
                                            'excess_heat',
                                            excess_heat_fluid,
                                            excess_heat_supply_temperature,
                                            excess_heat_target_temperature,
                                            excess_heat_flowrate,
                                            excess_heat_supply_capacity,
                                            schedule))

