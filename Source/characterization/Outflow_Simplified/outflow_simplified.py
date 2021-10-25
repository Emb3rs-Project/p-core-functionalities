"""
@author: jmcunha/alisboa

Info: Generate Outflow Simplified characteristics and hourly generation profile
      Schedule with 1h time steps.

Input: Source stream with calendar and characteristics
Output: Source stream updated with hourly profile, return temperature and capacity

"""

from General.Auxiliary_General.schedule_hour import schedule_hour


class Outflow_Simplified():

    def __init__(self,in_var):

        # Define var
        self.id = in_var.id
        self.stream_type = 'excess_heat'  # e.g. inflow, supply_heat, excess_heat

        # INPUT
        saturday_on = in_var.saturday_on
        sunday_on = in_var.sunday_on
        shutdown_periods = in_var.shutdown_periods
        daily_periods = in_var.daily_periods
        self.flowrate = in_var.flowrate
        self.supply_temperature = in_var.supply_temperature
        self.fluid_cp = in_var.fluid_cp
        self.fluid = in_var.fluid

        # COMPUTE
        # Schedule
        self.hourly_generation = schedule_hour(saturday_on,sunday_on,shutdown_periods,daily_periods)

        # Excess Heat
        self.target_temperature = in_var.target_temperature

        self.supply_capacity = self.flowrate * self.fluid_cp * (self.supply_temperature - self.target_temperature) / 3600  # kW

        if self.supply_capacity < 0:
            self.supply_capacity = 0



