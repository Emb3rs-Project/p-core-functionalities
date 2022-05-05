"""
alisboa/jmcunha


##############################
INFO: Adjust heating/cooling profiles according to user input


##############################
INPUT:
    'user_monthly_capacity' - platform user input
    'stream' - building or greenhouse streams


##############################
OUTPUT: stream with data corrected

"""

from ...Error_Handling.error_adjust_capacity import PlatformAdjustCapacity
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


def adjust_capacity(in_var):
    ###############################################################
    # INPUT
    # error handling
    platform_data = PlatformAdjustCapacity(**in_var['platform'])

    if platform_data.user_monthly_capacity is not None:
        user_monthly_capacity = vars(platform_data.user_monthly_capacity)
    else:
        user_monthly_capacity = platform_data.user_monthly_capacity

    user_yearly_capacity = platform_data.user_yearly_capacity
    stream = vars(platform_data.stream)

    ###############################################################
    # COMPUTE
    months_coef = {}

    try:
        if user_monthly_capacity is not None:
            for index, month_capacity in enumerate(stream['monthly_generation']):
                if user_monthly_capacity[str(months[index])] is None:
                    months_coef[months[index]] = 1
                else:
                    months_coef[months[index]] = user_monthly_capacity[str(months[index])] / month_capacity
            stream = monthly_adjust(stream, months_coef)

        else:
            for index, month_capacity in enumerate(stream['monthly_generation']):
                months_coef[months[index]] = user_yearly_capacity / sum(stream['monthly_generation'])

            stream = monthly_adjust(stream, months_coef)

    except:
        raise ModuleRuntimeException(
            code="1",
            type="adjust_capacity.py",
            msg="Adjusting the capacities was infeasible. Please check your inputs. \n "
                "If all inputs are correct report to the platform."
        )

    return stream


def monthly_adjust(stream, months_coef):
    hour_new_month = 0
    for index, month in enumerate(months):
        monthly_coef = months_coef[str(month)]

        if month == ('january' or 'march' or 'may' or 'july' or 'august' or 'october' or 'december'):
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
