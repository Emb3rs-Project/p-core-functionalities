from ...Error_Handling.runtime_error import ModuleRuntimeException

months = [
    "january"
    , "february"
    , "march"
    , "april"
    , "may"
    , "june"
    , "july"
    , "august"
    , "september"
    , "october"
    , "november"
    , "december"
]


def adjust_capacity(stream, user_daily_capacity=None, user_monthly_capacity=None, user_yearly_capacity=None):

    """ Adjust hourly capacity

    Adjust hourly capacity according to user real data

    Parameters
    ----------
    stream: dict
        Stream data

    user_daily_capacity: list:
        Real capacity for each hour of the year [kWh]

    user_monthly_capacity: dict
        Real capacity of each month [kWh]

    user_yearly_capacity: float
        Real yearly capacity [kWh]

    Returns
    -------
    stream: dict
       Stream data with the key "hourly_generation" adjusted to real data

    """


    ###############################################################
    # COMPUTE
    months_coef = {}
    try:

        if user_yearly_capacity is None and user_daily_capacity is None and user_monthly_capacity is not None:

            for index, month_capacity in enumerate(stream['monthly_generation']):
                if user_monthly_capacity[str(months[index])] is None:
                    months_coef[months[index]] = 1
                else:
                    months_coef[months[index]] = user_monthly_capacity[str(months[index])] / month_capacity

            stream = monthly_adjust(stream, months_coef)

        elif user_yearly_capacity is not None and user_daily_capacity is None and user_monthly_capacity is None:
            for index, month_capacity in enumerate(stream['monthly_generation']):
                months_coef[months[index]] = user_yearly_capacity / sum(stream['monthly_generation'])

            stream = monthly_adjust(stream, months_coef)

        else:  # user_daily_capacity is not None
            stream = daily_adjust(stream, user_daily_capacity)
    except:
        raise ModuleRuntimeException(
            code="1",
            type="adjust_capacity.py",
            msg="Adjusting the capacities was infeasible. Please check your inputs. "
                "If all inputs are correct report to the platform."
        )

    return stream

def monthly_adjust(stream, months_coef):
    hour_new_month = 0
    for index, month in enumerate(months):
        monthly_coef = months_coef[str(month)]

        if month == 'january' or month =='march' or month =='may' or month =='july' or month =='august' or month =='october' or month =='december':
            number_days = 31
        elif month == 'february':
            number_days = 29  # year with 366 days considered
        else:
            number_days = 30

        initial = hour_new_month
        final = hour_new_month + number_days * 24

        if month != 'december':
            stream["hourly_generation"][initial:final] = [round(i * monthly_coef,2) for i in
                                                          stream["hourly_generation"][initial:final]]
        else:
            stream["hourly_generation"][initial:] = [round(i * monthly_coef, 2)for i in
                                                     stream["hourly_generation"][initial:]]
        hour_new_month = final

        stream['monthly_generation'][index] = round(stream['monthly_generation'][index] * monthly_coef, 2)


    return stream


def daily_adjust(stream, daily_real_values):
    hour_new = 0
    daily_coef = []

    # get daily_coef
    for index, day_val in enumerate(daily_real_values):
        initial = hour_new
        final = hour_new + 24

        if final > len(daily_real_values) * 24:
            final = len(daily_real_values)

        theo_daily_val = sum(stream["hourly_generation"][initial:final])
        coef = day_val/theo_daily_val
        daily_coef.append(coef)

    # assure it's 366 days
    while len(daily_coef) < 366:
        daily_coef.append(daily_coef[-1])

    # adjust hourly profile
    hour_new = 0
    for index, day_coef in enumerate(daily_coef):
        initial = hour_new
        final = hour_new + 24

        if final > len(stream["hourly_generation"])-1:
            final = len(stream["hourly_generation"])-1

        stream["hourly_generation"][initial:final] = [round(i * day_coef,2) for i in stream["hourly_generation"][initial:final]]
        hour_new = final


    # get monthly generation
    hour_new_month = 0
    monthly_generation = []
    for index, month in enumerate(months):
        if month == 'january' or month =='march' or month =='may' or month =='july' or month =='august' or month =='october' or month =='december':
            number_days = 31
        elif month == 'february':
            number_days = 29  # year with 366 days considered
        else:
            number_days = 30

        initial = hour_new_month
        final = hour_new_month + number_days * 24

        if month != 'december':
            monthly_generation.append(sum(stream["hourly_generation"][initial:final]))
        else:
            monthly_generation.append(sum(stream["hourly_generation"][initial:]))

        hour_new_month = final

    stream["monthly_generation"] = monthly_generation
    return stream