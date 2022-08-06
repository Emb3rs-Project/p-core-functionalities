import datetime


def weekdays_daily_periods(daily_periods):
    cycle_start_time = []
    cycle_end_time = []

    for period in daily_periods:
        cycle_start_time.append(period[0])
        cycle_end_time.append(period[-1])

    return {"cycle_start_time": cycle_start_time, "cycle_end_time": cycle_end_time}


def schedule_hour_detailed(monday_daily_periods,
                           tuesday_daily_periods,
                           wednesday_daily_periods,
                           thursday_daily_periods,
                           friday_daily_periods,
                           saturday_daily_periods,
                           sunday_daily_periods,
                           shutdown_periods):

    # Shutdown Periods FROM USER - e.g. shutdown_periods = [[210,240], [255,290]]
    shutdown_start_date = []
    shutdown_end_date = []

    for period in shutdown_periods:
        shutdown_start_date.append(period[0])
        shutdown_end_date.append(period[-1])


    # Daily Working Periods FROM USER - e.g. daily_periods = [[8,12],[14,18]]

    week_daily_periods = {
                          '0': weekdays_daily_periods(monday_daily_periods),
                          '1': weekdays_daily_periods(tuesday_daily_periods),
                          '2': weekdays_daily_periods(wednesday_daily_periods),
                          '3': weekdays_daily_periods(thursday_daily_periods),
                          '4': weekdays_daily_periods(friday_daily_periods),
                          '5': weekdays_daily_periods(saturday_daily_periods),
                          '6': weekdays_daily_periods(sunday_daily_periods)
                          }
    # Initialize Arrays
    last_year = 2024
    year_hours = int(datetime.date(last_year, 12, 31).timetuple().tm_yday*24)  # Number of hours on that specific year
    profile_hour = [0] * year_hours
    day = [0] * year_hours
    hday = [0] * year_hours
    week = [0] * year_hours
    weekday = [0] * year_hours

    weekday[0] = datetime.date(last_year, 1, 1).weekday() + 1  # Weekday of 1st day of the year


    # Generate Profile
    for i in range(year_hours):
        op = 1  # on operation
        day[i] = round((i - 11.9) / 24) + 1  # day starting at 1 - 1st January
        hday[i] = i - (day[i] - 1) * 24  # hour starting at 0 - 00:00
        week[i] = round((day[i] - 3.51 + weekday[0]) / 7)
        weekday[i] = (day[i] - 1) - week[i] * 7 + weekday[0]

        # Check if Shutdown/Holiday Periods
        for j in range(len(shutdown_periods)):
            if shutdown_start_date[j] <= day[i] < shutdown_end_date[j]:
                op = 0
                break

        # Check if Weekend
        if op != 0:

            daily_periods = week_daily_periods[str(weekday[i])]

            # Check if Daily Operation Periods
            if op != 0:
                for j in range(len(daily_periods["cycle_start_time"])):
                    if daily_periods["cycle_start_time"][j] <= hday[i] < daily_periods["cycle_end_time"][j]:
                        op = 1
                        break
                    else:
                        op = 0

            if daily_periods["cycle_start_time"] == [] and daily_periods["cycle_end_time"] == []:
                profile_hour[i] = 0
            else:
                profile_hour[i] = op


    return profile_hour
