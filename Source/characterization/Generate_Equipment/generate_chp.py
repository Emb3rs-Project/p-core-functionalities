"""
@author: jmcunha/alisboa
"""

from General.Auxiliary_General.schedule_hour import schedule_hour
from General.Auxiliary_General.combustion import T_flue_gas,combustion_mass_flows
from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from General.Auxiliary_General.stream import Stream



class Chp():

    def __init__(self,in_var):


        # Defined Vars
        self.id = 50
        self.object_type = 'equipment'
        self.streams = []
        self.excess_heat_fluid = 'flue_gas'  # Excess heat fluid type
        self.inflow_T_in = self.excess_heat_return_temperature = 20  # Ambient Temperature

        # INPUT Equipment Characteristics FROM USER
        # self.electrical_generation = in_var.electrical_generation  # Generate_in_var electrical_generation [kW]
        # self.supply_temperature = in_var.supply_temperature

        self.equipment_sub_type = in_var.equipment_sub_type  # CHP type (gas_engine/ gas_turbine)
        self.open_closed_loop = in_var.open_closed_loop  # Open heating circuit? (1-Yes, 0-No)
        self.fuel_type = in_var.fuel_type  # Fuel type  (Natural gas, Fuel oil, Biomass)

        if self.open_closed_loop == 1:
            self.return_temperature = 20  # KB_General
        else:
            self.return_temperature = in_var.return_temperature  # [ºC]

        # Generate_in_var Characteristics FROM KB_General/USER
        self.global_conversion_efficiency = in_var.global_conversion_efficiency
        self.thermal_conversion_efficiency = in_var.thermal_conversion_efficiency
        self.supply_fluid = in_var.supply_fluid
        self.excess_heat_fluid = in_var.excess_heat_fluid
        self.electrical_conversion_efficiency = self.global_conversion_efficiency - self.thermal_conversion_efficiency


        # Schedule
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods
        daily_periods = in_var.daily_periods
        self.schedule = schedule_hour(saturday_on,
                                               sunday_on,
                                               shutdown_periods,
                                               daily_periods)




    def update_supply_capacity(self, supply_capacity):

        self.supply_capacity = supply_capacity  # [kW]
        self.electrical_generation = self.supply_capacity/self.thermal_conversion_efficiency*self.electrical_conversion_efficiency # [kW]

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
        fuel_consumption, m_air, m_flue_gas = combustion_mass_flows(self.supply_capacity,
                                                                    self.thermal_conversion_efficiency,
                                                                    self.fuel_type)

        # Inflow
        self.inflow_flowrate = m_air

        # Compute Eletrical Generation
        self.electrical_generation = self.supply_capacity/self.thermal_conversion_efficiency* self.electrical_conversion_efficiency # Generate_in_var electrical_generation [kW]

        thermal_capacity = self.electrical_generation / self.electrical_conversion_efficiency


        # Excess Heat
        # Supply Temperature [ºC]
        if self.equipment_sub_type == "gas_engine" or self.equipment_sub_type == "gas_turbine":
            self.excess_heat_supply_temperature, self.inflow_T_final = T_flue_gas(self.supply_capacity,
                                                                                  self.fuel_type, fuel_consumption,
                                                                                  m_flue_gas)
        else:
            self.supply_capacity = 0
            self.excess_heat_supply_temperature = 20


        # Supply Capacity [kW]
        self.excess_heat_supply_capacity = thermal_capacity - self.supply_capacity - self.electrical_generation

        # Flowrate [kg/h]
        self.excess_heat_flowrate = compute_flow_rate(self.excess_heat_fluid,
                                                      self.excess_heat_supply_capacity,
                                                      self.excess_heat_supply_temperature,
                                                      self.excess_heat_return_temperature)

        # Supply Heat
        # Flowrate [kg/h]
       # self.supply_flowrate = compute_flow_rate(self.supply_fluid,
        #                                         self.supply_capacity,
         #                                        self.supply_temperature,
          #                                       self.return_temperature)

    def output_stream(self):

        # inflow defined
        self.streams.append(Stream(self.id,
                                   'inflow',
                                   'air',
                                   self.inflow_T_in,
                                   self.inflow_T_final,
                                   self.inflow_flowrate,
                                   self.supply_capacity,
                                   self.schedule))

       # self.streams.append(Stream(self.id,
        #                           'supply_heat',
         #                          self.supply_fluid,
          #                         self.return_temperature,
           #                        self.supply_temperature,
            #                       self.supply_flowrate,
             #                      self.supply_capacity,
              #                     self.schedule))

        self.streams.append(Stream(self.id,
                                   'excess_heat',
                                   self.excess_heat_fluid,
                                   self.excess_heat_supply_temperature,
                                   self.excess_heat_return_temperature,
                                   self.excess_heat_flowrate,
                                   self.excess_heat_supply_capacity,
                                   self.schedule))




