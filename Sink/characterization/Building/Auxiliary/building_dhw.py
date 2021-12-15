"""
alisboa/jmcunha


##############################
INFO: Computes domestic hot water flowrate [m3/s] needed for each time step, and the total volume [m3] of water consumed
      until the considered time step.


##############################
INPUT:
        # hour
        # volume_dhw_set - max water volume allowed per day  [m3]
        # volume_dhw - last time_step water volume  [m3]
        # flowrate_dhw_set - water flowrate allowed  [m3/s]
        # time_step  [s]

##############################
OUTPUT:
        # flowrate [m3/s]
        # volume_dhw - current time_step water volume  [m3]


"""


def building_dhw(hour, volume_dhw_set, volume_dhw, flowrate_dhw_set, time_step):

    # get hour
    day = round((hour - 11.9) / 24) + 1  # day number; e.g. 1 - 1st January
    hour = hour - (day - 1) * 24  # hour; e.g. 0 - 00:00

    if 8 <= hour <= 9:
        flowrate = flowrate_dhw_set  # [m3/s]
        volume_dhw = volume_dhw + flowrate * time_step  # [m3]

        if volume_dhw >= 0.4 * volume_dhw_set:  # assumed max 40% consumption in the morning
            volume_dhw = volume_dhw - flowrate * time_step
            flowrate = 0

    elif 12 <= hour <= 13:
        flowrate = flowrate_dhw_set
        volume_dhw = volume_dhw + flowrate * time_step
        if volume_dhw >= 0.6 * volume_dhw_set:
            volume_dhw = volume_dhw - flowrate * time_step
            flowrate = 0

    elif 19 <= hour <= 20:
        flowrate = flowrate_dhw_set
        volume_dhw = volume_dhw + flowrate * time_step
        if volume_dhw >= volume_dhw_set:
            volume_dhw = volume_dhw - flowrate * time_step
            flowrate = 0

    elif hour >= 23:
        volume_dhw = 0
        flowrate = 0

    else:
        flowrate = 0

    return flowrate, volume_dhw
