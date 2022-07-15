from ....General.Auxiliary_General.stream_industry import stream_industry
import datetime
from ....utilities.kb import KB

class Process:

    def __init__(self,in_var, kb : KB):

        """
        Create Process object and characterize its streams (Inflow/Outflow/Maintenance/Evaporation).

        :param in_var: ``dict``: Process characterization data with the following keys:

                - id: ``int``: process ID []
                - equipment_id: ``int``: associated equipment ID []
                - operation_temperature: ``float``: process temperature [ºC]
                - saturday_on: ``int``: if it is available on Saturday []; 1 (yes)  or 0 (no)
                - sunday_on: ``int``: if it is available on Sunday []; 1 (yes)  or 0 (no)
                - shutdown_periods: ``list``: list with lists of periods of days it is not available [day]; e.g. [[130,140],[289,299]]
                - daily_periods: ``list``: list with lists of hourly periods it is available [h]; e.g. [[8,12],[15,19]]
                - schedule_type: ``str``: process schedule type; batch (1) or continuous (0)
                - cycle_time_percentage: ``float``: cycle  percentage for Startup/Inflow/Outflow during batch process
                - inflow_data: ``list with dict``: inflow ``dict`` with the following keys:

                    - name: ``str``: inflow name
                    - mass: ``float``: [OPTIONAL] inflow mass [kg]
                    - flowrate: ``float``: [OPTIONAL] inflow flowrate [kg/h]
                    - fluid_cp: ``float``: inflow cp [kJ/kg.K]
                    - supply_temperature: ``float``: inflow supply/initial temperature [ºC]

                - outflow_data ``list with dict``

                    - fluid_cp: ``float``: outflow cp [kJ/kg.K]
                    - target_temperature: ``float``: outflow target/final temperature [ºC]
                    - flowrate: ``float``: [OPTIONAL] outflow mass flowrate [kg/h]
                    - mass: ``float``: [OPTIONAL] outflow mass [kg]
                    - initial_temperature: ``float``: [OPTIONAL] outflow iniital temperature [ºC]

                - maintenance_data ``list with dict``

                    - name: ``str``: inflow name
                    - maintenance_capacity: ``float``: maintenance or evaporation capacity [kW]

        :param kb: Knowledge Base data

        """

        # defined var
        self.object_type = 'process'
        self.streams = []
        self.stream_id = 1

        # INPUT
        self.id = in_var['id']  # process ID
        self.equipment_id = in_var['equipment_id']  # heat/cool equipment id associated to
        self.operation_temperature = in_var['operation_temperature']
        self.saturday_on = in_var['saturday_on']
        self.sunday_on = in_var['sunday_on']
        self.shutdown_periods = in_var['shutdown_periods']  # e.g: [[59,74],[152,172],[362,365]]
        self.daily_periods = in_var['daily_periods']  # e.g: [[8,12],[15,19]]
        self.schedule_type = in_var['schedule_type']  # 0-Continuous, 1-Batch
        self.example_of_daily_period = self.daily_periods[0][1] - self.daily_periods[0][0]
        self.eff_equipment = in_var['eff_equipment']
        self.fuel = in_var['fuel_type']

        # Cycle percentage for Startup and Outflow (when in Batch)
        try:
            self.cycle_time_percentage = in_var['cycle_time_percentage']
            if self.cycle_time_percentage >= 1 or self.cycle_time_percentage <= 0:
                self.cycle_time_percentage = 0.1
        except:
            self.cycle_time_percentage = 0.1



        # Set Point Maintenance/ Evaporation
        try:
            maintenance_data = in_var['maintenance_data']
            self.generate_maintenance_and_evaporation(maintenance_data)
        except:
            pass

        # Inflows
        try:
            inflow_data = in_var['inflow_data']
            self.generate_inflow(inflow_data)
        except:
            pass

        # Outflows
        outflow_data = in_var['outflow_data']
        self.generate_outflow(outflow_data)

    def generate_maintenance_and_evaporation(self,data):

        # Maintenance/Evaporation Info
        for maintenance in data:
            schedule = self.schedule('maintenance')

            self.streams.append(stream_industry(maintenance['name'],
                                                self.id,
                                                'maintenance',
                                                "water",
                                                self.operation_temperature - 1,
                                                self.operation_temperature + 1,
                                                None,
                                                maintenance['maintenance_capacity'],
                                                schedule,
                                                stream_id=self.stream_id,
                                                fuel=self.fuel,
                                                eff_equipment=self.eff_equipment
                                                ))

            self.stream_id += 1

    def generate_inflow(self,data):

        schedule = self.schedule('inflow')

        for inflow in data:
            try:  # batch
                capacity = inflow['mass'] / (self.example_of_daily_period * 3600) * inflow['fluid_cp'] * (self.operation_temperature - inflow['supply_temperature'])  # [kW]
            except:
                capacity = inflow['flowrate'] / 3600 * inflow['fluid_cp'] * (self.operation_temperature - inflow['supply_temperature'])  # [kW]

            self.streams.append(stream_industry(inflow['name'],
                                                self.id,
                                                'inflow',
                                                inflow['fluid'],
                                                inflow['supply_temperature'],
                                                self.operation_temperature,
                                                inflow['flowrate'],
                                                capacity,
                                                schedule,
                                                stream_id=self.stream_id,
                                                fuel=self.fuel,
                                                eff_equipment=self.eff_equipment
                                                ))

            self.stream_id += 1

    def generate_outflow(self,outflow_data):

        schedule = self.schedule('outflow')

        for outflow in outflow_data:
            try:  # batch
                capacity = outflow['flowrate'] / 3600 * outflow['fluid_cp'] * (self.operation_temperature - outflow['target_temperature'])  # [kW]
            except:
                capacity = outflow['mass'] / (self.example_of_daily_period * self.cycle_time_percentage * 3600) * outflow['fluid_cp'] * (self.operation_temperature - outflow['target_temperature'])  # [kW]

            if outflow["initial_temperature"] == None:
                initial_temperature = self.operation_temperature
            else:
                initial_temperature = outflow["initial_temperature"]


            self.streams.append(stream_industry(outflow['name'],
                                                self.id,
                                                'outflow',
                                                outflow['fluid'],
                                                initial_temperature,
                                                outflow['target_temperature'],
                                                outflow['flowrate'],
                                                capacity,
                                                schedule,
                                                stream_id=self.stream_id,
                                                fuel="none",
                                                eff_equipment=None
                                                ))

            self.stream_id += 1



    def schedule(self,stream_type):

        # Shutdown Periods
        shutdown_start_date = []
        shutdown_end_date = []
        for period in self.shutdown_periods:
            shutdown_start_date.append(period[0].timetuple().tm_yday)
            shutdown_end_date.append(period[-1].timetuple().tm_yday)

        # Cycle Working Periods
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
