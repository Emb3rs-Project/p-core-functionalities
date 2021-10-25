"""
@author: jmcunha/alisboa

Info: Generate Process.

Input: Process schedule and characteristics (inflows, outflows, startup, maintenance, operation temperature, schedule type)

Return: Process object

"""

from General.Auxiliary_General.stream import Stream
import numpy as np
import datetime


class Process:

    def __init__(self,in_var):

        # defined var
        self.object_type = 'process'
        self.streams = []
        self.id = 56

        # Process Characteristics
        self.equipment = in_var.equipment # heat/cool equipment id associated to
        self.operation_temperature = in_var.operation_temperature


        # Schedule Process FROM USER OR INVAR ASSUMES MASTER SCHEDULE
        self.saturday_on = in_var.saturday_on
        self.sunday_on = in_var.sunday_on
        self.shutdown_periods = in_var.shutdown_periods
        self.daily_periods = in_var.daily_periods
        self.schedule_type = in_var.schedule_type  # 0-Continuous, 1-Batch
        self.cycle_time_percentage = in_var.cycle_time_percentage # Cycle percentage for Startup and Outflow (when in Batch)

        # Startup
        startup_data = in_var.startup_data
        if startup_data != []:
            self.generate_process_startup(startup_data)

        # Maintenance
        maintenance_data = in_var.maintenance_data
        if maintenance_data != []:
            self.generate_process_maintenance(maintenance_data)

        # Inflows
        inflow_data = in_var.inflow_data
        if inflow_data != []:
            self.generate_process_inflow(inflow_data)

        # Outflows
        outflow_data = in_var.outflow_data
        if outflow_data != []:
            self.generate_process_outflow(outflow_data)


    def generate_process_startup(self,startup_data):

        # Startup
        for startup in startup_data:
            startup_fluid = startup.fluid
            startup_T_initial = startup.T_initial
            startup_mass = startup.mass  # [kg]
            startup_fluid_cp = startup.fluid_cp

            # Schedule
            hourly_generation = self.schedule('startup')

            startup_capacity = startup_mass/self.cycle_time_percentage * startup_fluid_cp * (self.operation_temperature-startup_T_initial)  # [kW]

            self.streams.append(Stream(self.id,'startup',
                                       startup_fluid,
                                       startup_T_initial,
                                       self.operation_temperature,
                                       startup_mass/self.cycle_time_percentage,
                                       startup_capacity,
                                       hourly_generation))


    def generate_process_maintenance(self,maintenance_data):

        # Maintenance Info
        for maintenance in maintenance_data:
            maintenance_capacity = maintenance.capacity

            # Schedule
            hourly_generation = self.schedule('maintenance')

            self.streams.append(Stream(self.id,
                                       'maintenance',
                                       'none',
                                       0,
                                       0,
                                       maintenance_capacity,
                                       0,
                                       hourly_generation))


    def generate_process_inflow(self,inflow_data):

        # Schedule
        hourly_generation = self.schedule('inflow')

        for inflow in inflow_data:
            inflow_fluid = inflow.fluid
            inflow_supply_temperature = inflow.supply_temperature  # [ºC]
            inflow_target_temperature = self.operation_temperature  # [ºC]
            inflow_flowrate = inflow.flowrate  # [kg/h]
            inflow_fluid_cp = inflow.fluid_cp  # [kJ/kg.K]

            capacity = inflow.flowrate * inflow_fluid_cp * (inflow_target_temperature - inflow_supply_temperature)/3600  # [kW]

            self.streams.append(Stream(self.id,'inflow',
                                       inflow_fluid,
                                       inflow_supply_temperature,
                                       inflow_target_temperature,
                                       inflow_flowrate,
                                       capacity,
                                       hourly_generation))


    def generate_process_outflow(self,outflow_data):

        # Schedule
        hourly_generation = self.schedule('outflow')

        for outflow in outflow_data:
            outflow_fluid = outflow.fluid
            outflow_supply_temperature = self.operation_temperature
            outflow_target_temperature = outflow.target_temperature
            outflow_flowrate = outflow.flowrate
            outflow_fluid_cp = outflow.fluid_cp

            capacity = outflow_flowrate * outflow_fluid_cp * (outflow_supply_temperature - outflow_target_temperature)/3600  # [kW]

            self.streams.append(Stream(self.id,'outflow',
                                       outflow_fluid,
                                       outflow_supply_temperature,
                                       outflow_target_temperature,
                                       outflow_flowrate,
                                       capacity,
                                       hourly_generation))


    def schedule(self,stream_type):

        # Shutdown Periods FROM USER - e.g. shutdown_periods = [[1/jan/2021,6/jan/2021],[3/aug/2021,10/aug/2021]]
        shutdown_start_date = []
        shutdown_end_date = []
        for period in self.shutdown_periods:
            shutdown_start_date.append(period[0].timetuple().tm_yday)
            shutdown_end_date.append(period[-1].timetuple().tm_yday)

        # Cycle Working Periods FROM USER - e.g. daily_periods = [[8,12],[14,18]]
        cycle_start_time = []
        cycle_end_time = []
        cycle_duration = []
        for period in self.daily_periods:
            cycle_start_time.append(period[0])
            cycle_end_time.append(period[-1])
            cycle_duration.append(period[-1] - period[0])

        # Initialize Arrays
        now = datetime.datetime.now()
        last_year = now.year - 1
        year_10min = int(
            datetime.date(last_year, 12, 31).timetuple().tm_yday * 24 * 6)  # number of 10min on that specific year
        year_hour = int(datetime.date(last_year, 12, 31).timetuple().tm_yday * 24)

        profile_10min = [0] * year_10min
        profile_hour = []
        day = [0] * year_10min
        hday = [0] * year_10min
        tenminday = [0] * year_10min
        week = [0] * year_10min
        weekday = [0] * year_10min

        weekday[0] = datetime.date(last_year, 1, 1).weekday() + 1  # Weekday of 1st day of the year

        # Generate Profile
        hour_old = 0
        for i in range(year_10min):
            op = 1  # on operation

            day[i] = round((i - 11.9 * 6) / (24 * 6)) + 1  # day starting at 1 - 1st January
            hday[i] = int((i - (day[i] - 1) * 24 * 6) * 1 / 6)  # hour starting at 0 - 00:00 -> e.g [0,...,23]
            tenminday[i] = (i - (day[
                                     i] - 1) * 24 * 6) * 1 / 6  # 10 min starting at 0 - 00:00 -> e.g [0,0.16(6),0.3(3),...,23.83(3)]
            week[i] = round((day[i] - 3.5 + weekday[0]) / 7)
            weekday[i] = (day[i] - 1) - week[i] * 7 + weekday[0]

            # Check if Shutdown/Holiday Periods
            for j in range(len(self.shutdown_periods)):
                if shutdown_start_date[j] <= day[i] < shutdown_end_date[j]:
                    op = 0
                    break

            # Check if Weekend
            if weekday[i] == 6 and op != 0:
                op *= self.saturday_on
            elif weekday[i] == 7 and op != 0:
                op *= self.sunday_on

            # Check if Daily Operation Periods
            if (self.schedule_type == 1 and stream_type == 'inflow' ) or stream_type == 'startup':
                if op != 0:
                    for j in range(len(self.daily_periods)):

                        if cycle_start_time[j] <= tenminday[i] < cycle_start_time[j] + cycle_duration[j] * self.cycle_time_percentage:
                            op = 1
                            break
                        else:
                            op = 0

            elif (self.schedule_type == 1 and stream_type == 'outflow' ):
                if op != 0:
                    for j in range(len(self.daily_periods)):
                        if cycle_end_time[j] <= tenminday[i] < cycle_end_time[j] + cycle_duration[j] * self.cycle_time_percentage:
                            op = 1
                            break
                        else:
                            op = 0

            else:
                if op != 0:
                    for j in range(len(self.daily_periods)):
                        if cycle_start_time[j] <= tenminday[i] < cycle_end_time[j]:
                            op = 1
                            break
                        else:
                            op = 0

            profile_10min[i] = op

            if hday[i] != hour_old:
                profile_hour.append(sum(profile_10min[(i - 6):i]) / len(profile_10min[(i - 6):i]))
                hour_old = hday[i]

        # OUTPUT
        profile_hourly = np.asarray(profile_hour)
        #profile_optimization = np.asarray(profile_10min)

        return profile_hourly
