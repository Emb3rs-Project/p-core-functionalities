import datetime

def schedule_hour(saturday_on,sunday_on,shutdown_periods,daily_periods):
    """Get operating schedule

    Receives user schedule data and returns 1h time step profile  of 1 (operating) and 0 (not operating).

    Parameters
    ----------
    saturday_on : int
        if available or not on Saturday; 1=yes, 0=no


    sunday_on : int
        if available or not on Sunday; 1=yes, 0=no


    shutdown_periods : list with lists
        List with list of shutdown days intervals, e.g, [[2,10],[361-365]]


    daily_periods : list with lists
        List with lists of daily intervals, e.g. [[9,12],[14,17]]


    Returns
    -------
    profile_hour : list
        Hourly schedule; with 1 and 0

    """

    # Shutdown Periods FROM USER - e.g. shutdown_periods = [[210,240], [255,290]]
    shutdown_start_date = []
    shutdown_end_date = []

    for period in shutdown_periods:
        shutdown_start_date.append(period[0])
        shutdown_end_date.append(period[-1])


    # Daily Working Periods FROM USER - e.g. daily_periods = [[8,12],[14,18]]
    cycle_start_time = []
    cycle_end_time = []

    for period in daily_periods:
        cycle_start_time.append(period[0])
        cycle_end_time.append(period[-1])



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
        if weekday[i] == 5 and op != 0:
            op *= saturday_on
        elif weekday[i] == 6 and op != 0:
            op *= sunday_on

        # Check if Daily Operation Periods
        if op != 0:
            for j in range(len(daily_periods)):
                if cycle_start_time[j] <= hday[i] < cycle_end_time[j]:
                    op = 1
                    break
                else:
                    op = 0

        if cycle_start_time == [] and cycle_end_time == []:
            profile_hour[i] = 0
        else:
            profile_hour[i] = op


    return profile_hour
