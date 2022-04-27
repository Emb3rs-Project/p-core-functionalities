"""
alisboa/jmcunha

##############################
INFO: Create Process object and characterize its streams.

##############################
INPUT: object with:

        # id  - process id
        # equipment - heat/cooling equipment id associated to
        # operation_temperature  # process operation_temperature [ºC]
        # saturday_on - 1 (yes)  or 0 (no)
        # sunday_on - 1 (yes)  or 0 (no)
        # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
        # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]
        # schedule_type  - 0=Continuous, 1=Batch
        # cycle_time_percentage  - Cycle percentage for Startup and Outflow; 0 to 0.9
        # startup_data - vector with dictionaries
        # maintenance_data - vector with dictionaries
        # inflow_data - vector with dictionaries
        # outflow_data - vector with dictionaries

         Where in startup_data :
             # fluid - fluid name
             # initial_temperature [ºC]
             # mass [kg]

         Where in maintenance_data :
             # capacity [kW]

        Where in inflow_data :
             # fluid - fluid name
             # supply_temperature [ºC]
             # flowrate [kg/h]

        Where in outflow_data :
             # fluid - fluid name
             # target_temperature [ºC]
             # flowrate [kg/h]


##############################
OUTPUT: object Process

        IMPORTANT:
         # process.streams important attribute for CF Internal Heat Recovery

"""

from ....General.Auxiliary_General.stream_industry import stream_industry
import datetime
from ....utilities.kb import KB

class Process:

    def __init__(self,in_var, kb : KB):

        # defined var
        self.object_type = 'process'
        self.streams = []

        # INPUT
        self.id = in_var['platform']['id']  # process ID
        self.equipment = in_var['platform']['equipment']  # heat/cool equipment id associated to
        self.operation_temperature = in_var['platform']['operation_temperature']
        self.saturday_on = in_var['platform']['saturday_on']
        self.sunday_on = in_var['platform']['sunday_on']
        self.shutdown_periods = in_var['platform']['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        self.daily_periods = in_var['platform']['daily_periods']  # e.g: [[8,12],[15,19]]
        self.schedule_type = in_var['platform']['schedule_type']  # 0-Continuous, 1-Batch



        try:
            self.cycle_time_percentage = in_var['platform']['cycle_time_percentage']  # Cycle percentage for Startup and Outflow (when in Batch)
            if self.cycle_time_percentage >= 1 or self.cycle_time_percentage <= 0:
                self.cycle_time_percentage = 0.1
        except:
            self.cycle_time_percentage = 0.1

        # Startup
        try:
            startup_data = in_var['platform']['startup_data']
            self.generate_process_startup(startup_data)
        except:
            pass

        # Maintenance
        try:
            maintenance_data = in_var['platform']['maintenance_data']
            self.generate_process_maintenance(maintenance_data)
        except:
            pass

        # Inflows
        try:
            inflow_data = in_var['platform']['inflow_data']
            self.generate_process_inflow(inflow_data)
        except:
            pass

        # Outflows
        try:
            outflow_data = in_var['platform']['outflow_data']
            self.generate_process_outflow(outflow_data)
        except:
            pass


    def generate_process_startup(self,data):

        for startup in data:

            schedule = self.schedule('startup')
            capacity = startup['mass']/self.cycle_time_percentage * startup['fluid_cp'] * (self.operation_temperature - startup['supply_temperature'])  # [kW]

            self.streams.append(stream_industry(self.id,
                                       'startup',
                                       startup['fluid'],
                                       startup['supply_temperature'],
                                       self.operation_temperature,
                                       startup['mass']/self.cycle_time_percentage,
                                       capacity,
                                       schedule))


    def generate_process_maintenance(self,data):

        # Maintenance Info
        for maintenance in data:
            schedule = self.schedule('maintenance')

            self.streams.append(stream_industry(self.id,
                                       'maintenance',
                                       'none',
                                       0,
                                       0,
                                       maintenance['maintenance_capacity'],
                                       0,
                                       schedule))


    def generate_process_inflow(self,data):

        schedule = self.schedule('inflow')

        for inflow in data:
            capacity = inflow['flowrate'] * inflow['fluid_cp'] * (self.operation_temperature - inflow['supply_temperature'])/3600  # [kW]
            self.streams.append(stream_industry(self.id,
                                       'inflow',
                                       inflow['fluid'],
                                       inflow['supply_temperature'],
                                       self.operation_temperature,
                                       inflow['flowrate'],
                                       capacity,
                                       schedule))


    def generate_process_outflow(self,outflow_data):

        schedule = self.schedule('outflow')

        for outflow in outflow_data:
            capacity = outflow['flowrate'] * outflow['fluid_cp'] * (self.operation_temperature - outflow['target_temperature'])/3600  # [kW]

            self.streams.append(stream_industry(self.id,'outflow',
                                       outflow['fluid'],
                                       self.operation_temperature,
                                       outflow['target_temperature'],
                                       outflow['flowrate'],
                                       capacity,
                                       schedule))


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
        year_10min = int(datetime.date(last_year, 12, 31).timetuple().tm_yday * 24 * 6)  # number of 10min on that specific year
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


        return profile_hour
