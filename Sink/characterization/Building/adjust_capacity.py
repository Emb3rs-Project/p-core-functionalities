"""
alisboa/jmcunha


##############################
INFO: Adjust heating/cooling profiles according to user input


##############################
INPUT:
    'user_heat_monthly_capacity' - platform user input
    'user_cold_monthly_capacity' - platform user input
    'streams' - building or greenhouse streams -> from the characterization routines ('hot_stream' and 'cold_stream')


##############################
OUTPUT: streams corrected

        Where for example:
        # 'hot_stream' = {
        #           'id' - stream id
        #           'object_type' - stream
        #           'fluid' - water
        #           'stream_type' - inflow
        #           'monthly_generation' - array [kWh]
        #           'hourly_generation' - array [kWh]
        #           'supply_temperature' [ºC]
        #           'target_temperature' [ºC]
        #           }



"""


def adjust_capacity(in_var):


    ###############################################################
    # INPUT
    user_heat_monthly_capacity = in_var['platform']['user_heat_monthly_capacity']
    user_cold_monthly_capacity = in_var['platform']['user_cold_monthly_capacity']
    streams_dict = in_var['cf_module']['streams']


    ###############################################################
    # COMPUTE
    hot_stream = streams_dict['hot_stream']
    cold_stream = streams_dict['cold_stream']

    try:
        hour_new_month = 0
        for index, user_heat_monthly in enumerate(user_heat_monthly_capacity):
            monthly_coef = user_heat_monthly / hot_stream['monthly_generation']

            month = index + 1
            if month == (1 or 3 or 5 or 7 or 8 or 10 or 12):
                number_days = 31
            elif month == 2:
                number_days = 29 # year with 366 days considered
            else:
                number_days = 30

            initial = hour_new_month
            final = hour_new_month + number_days * 24

            if month != 12:
                hot_stream["hourly_generation"][initial:final] = [i* monthly_coef for i in hot_stream["hourly_generation"][initial:final]]
            else:
                hot_stream["hourly_generation"][initial:] = [i* monthly_coef for i in hot_stream["hourly_generation"][initial:]]

            hour_new_month = final

    except:
        pass

    try:
        hour_new_month = 0
        for index, user_cold_monthly in enumerate(user_cold_monthly_capacity):
            monthly_coef = user_cold_monthly / hot_stream['monthly_generation']

            month = index + 1
            if month == (1 or 3 or 5 or 7 or 8 or 10 or 12):
                number_days = 31
            elif month == 2:
                number_days = 29 # year with 366 days considered
            else:
                number_days = 30

            initial = hour_new_month
            final = hour_new_month + number_days * 24

            if month != 12:
                cold_stream["hourly_generation"][initial:final] = [i * monthly_coef for i in cold_stream["hourly_generation"][initial:final]]
            else:
                cold_stream["hourly_generation"][initial:] = [i * monthly_coef for i in cold_stream["hourly_generation"][initial:]]

            hour_new_month = final
    except:
        pass


    try:
        hot_stream['monthly_generation'] = user_heat_monthly_capacity
    except:
        pass

    try:
        cold_stream['monthly_generation'] = user_cold_monthly_capacity
    except:
        pass


    corrected_streams = {
        'hot_stream': hot_stream,
        'cold_stream': cold_stream
    }

    return corrected_streams
