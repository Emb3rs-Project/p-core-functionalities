import datetime


def month_last_hour():
    """Get month last hour correspondent number

    E.g 31st Jan at 23h = 744

    Returns
    -------
    list
        hour for each month

    """
    now = datetime.datetime.now()
    year = 2020  # leap year

    jan = datetime.datetime(year, 1, 31, 23,
                            0).timetuple().tm_yday * 24 - 1  # get last month hour (subtract 1 to match profile hour index 0-23)
    feb = datetime.datetime(year, 2, 28, 23, 0).timetuple().tm_yday * 24 - 1
    mar = datetime.datetime(year, 3, 31, 23, 0).timetuple().tm_yday * 24 - 1
    apr = datetime.datetime(year, 4, 30, 23, 0).timetuple().tm_yday * 24 - 1
    may = datetime.datetime(year, 5, 31, 23, 0).timetuple().tm_yday * 24 - 1
    jun = datetime.datetime(year, 6, 30, 23, 0).timetuple().tm_yday * 24 - 1
    jul = datetime.datetime(year, 7, 31, 23, 0).timetuple().tm_yday * 24 - 1
    aug = datetime.datetime(year, 8, 31, 23, 0).timetuple().tm_yday * 24 - 1
    sep = datetime.datetime(year, 9, 30, 23, 0).timetuple().tm_yday * 24 - 1
    oct = datetime.datetime(year, 10, 31, 23, 0).timetuple().tm_yday * 24 - 1
    nov = datetime.datetime(year, 11, 30, 23, 0).timetuple().tm_yday * 24 - 1
    dec = datetime.datetime(year, 12, 31, 23, 0).timetuple().tm_yday * 24 - 1

    return [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
