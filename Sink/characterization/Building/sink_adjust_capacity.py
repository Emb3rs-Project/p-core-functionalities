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


def sink_adjust_capacity(in_var):

    ###############################################################
    # INPUT
    # error handling platform inputs

    user_monthly_capacity = in_var['platform']['user_monthly_capacity']
    stream = in_var['cf_module']['stream_building']

    ###############################################################
    # COMPUTE

    try:
        hour_new_month = 0
        for index, user_heat_monthly in enumerate(user_monthly_capacity):
            monthly_coef = user_heat_monthly / stream['monthly_generation']

            month = index + 1
            if month == (1 or 3 or 5 or 7 or 8 or 10 or 12):
                number_days = 31
            elif month == 2:
                number_days = 29  # year with 366 days considered
            else:
                number_days = 30

            initial = hour_new_month
            final = hour_new_month + number_days * 24

            if month != 12:
                stream["hourly_generation"][initial:final] = [i * monthly_coef for i in
                                                              stream["hourly_generation"][initial:final]]
            else:
                stream["hourly_generation"][initial:] = [i * monthly_coef for i in
                                                         stream["hourly_generation"][initial:]]
            hour_new_month = final
    except:
        pass

    try:
        stream['monthly_generation'] = user_monthly_capacity
    except:
        pass

    return stream


