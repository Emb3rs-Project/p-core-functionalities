"""
@author: jmcunha/alisboa

"""

from General.Auxiliary_General.schedule_hour import schedule_hour
from General.Auxiliary_General.combustion import T_flue_gas,combustion_mass_flows
from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from General.Auxiliary_General.stream import Stream

class Boiler():


    def __init__(self,in_var):

        # Defined Vars
        self.id = 1001 # Create ID for each boiler
        self.object_type = 'equipment'
        self.streams = []
        self.excess_heat_fluid = 'flue_gas'  # Excess heat fluid type
        self.inflow_T_initial = 20  # Ambient Temperature
        self.excess_heat_return_temperature = 20  # Ambient Temperature

        # INPUT
        self.equipment_sub_type = in_var.equipment_sub_type  # Boiler type (hot_water_boiler/ steam_boiler/ condensing_boiler)
        #self.supply_temperature = in_var.supply_temperature
        self.supply_capacity_nominal = in_var.supply_capacity_nominal  # Generate_Equipment heat supply capacity [kW]
        self.global_conversion_efficiency = in_var.global_conversion_efficiency

        # Schedule
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods # e.g: [[59,74],[152,172],[362,365]]
        daily_periods = in_var.daily_periods # e.g: [[8,12],[15,19]]
        self.schedule = schedule_hour(saturday_on,
                                               sunday_on,
                                               shutdown_periods,
                                               daily_periods)

        self.open_closed_loop = in_var.open_closed_loop  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = in_var.fuel_type  # Fuel type  (Natural gas, Fuel oil, Biomass)
        #self.supply_fluid = in_var.supply_fluid

        if self.open_closed_loop == 1:
            self.return_temperature = 20  # KB_General - Ambient Temperature
        else:
            self.return_temperature = in_var.return_temperature


    def update_supply_capacity(self, supply_capacity):

        self.supply_capacity = supply_capacity

        # Equipment
        self.equipment_characteristics()
        self.output_stream()


    def update_processes(self,processes):

        self.total_yearly_supply_capacity = 0

        if processes != []:
            for process in processes:
                for stream in process.streams:

                    if stream.stream_type == 'inflow' or stream.stream_type == 'maintenance':
                        self.total_yearly_supply_capacity += stream.capacity * sum(stream.schedule)

            self.supply_capacity = self.total_yearly_supply_capacity/(sum(self.schedule))

        else:
            self.supply_capacity = 0



            # Equipment
        self.equipment_characteristics()
        self.output_stream()


    def equipment_characteristics(self):

        # Fuel Consumption [kg/h]
        self.fuel_consumption,m_air,m_flue_gas = combustion_mass_flows (self.supply_capacity,
                                                                   self.global_conversion_efficiency,
                                                                   self.fuel_type)
        # Inflow
        self.inflow_flowrate = m_air


        # Supply Heat
        # Flowrate [kg/h]
        #self.supply_flowrate = compute_flow_rate(self.supply_fluid,
        #                                         self.supply_capacity,
        #                                         self.supply_temperature,
        #                                         self.return_temperature)

        # Excess Heat
        # Supply Capacity [kW]
        thermal_capacity = self.supply_capacity / self.global_conversion_efficiency
        self.excess_heat_supply_capacity = thermal_capacity - self.supply_capacity

        # Supply Temperature [ºC]
        self.excess_heat_supply_temperature, self.inflow_T_outlet = T_flue_gas(self.supply_capacity,
                                                                              self.fuel_type,
                                                                              self.fuel_consumption,
                                                                              m_flue_gas)

        # Flowrate [kg/h]
        self.excess_heat_flowrate = compute_flow_rate(self.excess_heat_fluid,
                                                      self.excess_heat_supply_capacity,
                                                      self.excess_heat_supply_temperature,
                                                      self.excess_heat_return_temperature)


    def output_stream(self):

        # Air Inflow
        self.streams.append(Stream(self.id,
                                   'inflow',
                                   'air',
                                   self.inflow_T_initial,
                                   self.inflow_T_outlet,
                                   self.inflow_flowrate,
                                   self.supply_capacity,
                                   self.schedule))

        # Supply Heat
        #self.streams.append(Stream(self.id,
        #                           'supply_heat',
        #                           self.supply_fluid,
        #                           self.return_temperature,
        #                           self.supply_temperature,
        #                           self.supply_flowrate,
        #                           self.supply_capacity,
        #                          self.schedule))

        # Excess Heat
        self.streams.append(Stream(self.id,
                                   'excess_heat',
                                   self.excess_heat_fluid,
                                   self.excess_heat_supply_temperature,
                                   self.excess_heat_return_temperature,
                                   self.excess_heat_flowrate,
                                   self.excess_heat_supply_capacity,
                                   self.schedule))







