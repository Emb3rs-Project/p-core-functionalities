"""
@author: jmcunha/alisboa

"""

from General.Auxiliary_General.schedule_hour import schedule_hour
from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from General.Auxiliary_General.stream import Stream
from General.Auxiliary_General.compute_cop_err import compute_cop_err

class Cooling_Equipment():


    def __init__(self,in_var):

        # Defined Vars
        self.id = 23
        self.object_type = 'equipment'
        self.streams = []

        # INPUT Equipment Characteristics FROM USER
        self.equipment_sub_type = in_var.equipment_sub_type  # Equipment type (co2_chiller/ cooling_tower/ thermal_chiller/ air_cooled_chiller/ water_cooled_chiller)
        self.supply_temperature = in_var.supply_temperature
        self.return_temperature = in_var.return_temperature
        self.fuel_type = 'electricity'  # Electricity
        self.global_conversion_efficiency = in_var.global_conversion_efficiency  # COP
        self.supply_fluid = 'water'

        if self.equipment_sub_type == 'co2_chiller':
            self.excess_heat_supply_temperature = in_var.excess_heat_supply_temperature
            self.excess_heat_return_temperature = in_var.excess_heat_return_temperature
            self.excess_heat_fluid = in_var.excess_heat_fluid  # Excess heat fluid type

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

        self.supply_capacity = supply_capacity  # Supply capacity [kW]

        # Equipment
        self.equipment_characteristics()
        self.output_stream()


    def update_processes(self, processes):

        self.total_yearly_supply_capacity = 0  # Supply capacity [kW]

        if processes != []:
            for process in processes:
                for stream in process.streams:
                    if stream.stream_type == 'inflow' or stream.stream_type == 'maintenance':
                        self.total_yearly_supply_capacity += stream.capacity * sum(stream.schedule)

            self.supply_capacity = self.total_yearly_supply_capacity / (sum(self.schedule))

        else:
            self.supply_capacity = 0

        # Equipment
        self.equipment_characteristics()
        self.output_stream()


    def equipment_characteristics(self):

        # Supply Heat
        # Flowrate [kg/h]
        self.supply_flowrate = compute_flow_rate(self.supply_fluid,
                                                 self.supply_capacity,
                                                 self.return_temperature,
                                                 self.supply_temperature)

        # Excess Heat
        if self.equipment_sub_type == 'co2_chiller':
            # Excess Heat Supply Capacity [kW]
            electrical_consumption = self.supply_capacity / self.global_conversion_efficiency
            self.excess_heat_supply_capacity = electrical_consumption + self.supply_capacity

            # Excess Heat Flowrate [kg/h]
            self.excess_heat_flowrate = compute_flow_rate(self.excess_heat_fluid,
                                                          self.excess_heat_supply_capacity,
                                                          self.excess_heat_supply_temperature,
                                                          self.excess_heat_return_temperature)

        else:
            self.excess_heat_supply_capacity = 0
            self.excess_heat_flowrate = 0



    def output_stream(self):

        self.streams.append(Stream(self.id,
                                   'supply_heat',
                                   self.supply_fluid,
                                   self.return_temperature,
                                   self.supply_temperature,
                                   self.supply_flowrate,
                                   self.supply_capacity,
                                   self.schedule))

        if self.equipment_sub_type == 'co2_chiller':
            self.streams.append(Stream(self.id,
                                       'excess_heat',
                                       self.excess_heat_fluid,
                                       self.excess_heat_supply_temperature,
                                       self.excess_heat_return_temperature,
                                       self.excess_heat_flowrate,
                                       self.excess_heat_supply_capacity,
                                       self.schedule))










