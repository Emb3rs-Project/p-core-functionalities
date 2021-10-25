""""

Info: Computes domestic hot water flowrate [m3/s] needed for each time step, and the volume [m3] of water consumed until the
 considered time step.

"""

def building_dhw(hour,volume_dhw_set,volume_dhw,flowrate_dhw_set,time_step):

    day = round((hour - 11.9) / 24) + 1  # day starting at 1 - 1st January
    hour = hour - (day - 1) * 24  # hour starting at 0 - 00:00

    if 8 <= hour <= 9:
        flowrate = flowrate_dhw_set  # [m3/s]
        volume_dhw = volume_dhw + flowrate * time_step  # [m3]

        if volume_dhw >= 0.4 * volume_dhw_set:  # Assumed MAX 40% consumein the morning
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



    return flowrate,volume_dhw