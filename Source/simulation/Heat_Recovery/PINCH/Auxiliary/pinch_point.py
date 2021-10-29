"""
@author: jmcunha/alisboa

Info: Get pinch point. Find where heat sum is minimum in heat cascade.

"""

import numpy as np

def pinch_point(df_gcc):

    heat_sum = 0
    minimum = 0
    pinch_temperature = 0
    net_heat_flow = [heat_sum]
    for index, temperature_interval in df_gcc[::-1].iterrows():

        heat_sum += temperature_interval["dH"] *10**(-3) #MJ/h
        net_heat_flow.append(heat_sum)

        # Get Pinch Point, where heat sum cascade is minimum
        if heat_sum < minimum:
            minimum = heat_sum
            pinch_temperature = index

    # Add heat in pinch point to new heat flow
    net_heat_flow = np.add(net_heat_flow, [abs(minimum)]*len(net_heat_flow))

    return pinch_temperature,net_heat_flow