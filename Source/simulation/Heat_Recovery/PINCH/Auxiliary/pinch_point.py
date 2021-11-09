""""
alisboa/jmcunha

##############################
INFO: Get pinch point. Find where heat sum is minimum in heat cascade.

##############################
INPUT:
        # df_heat_cascade - DF with heat cascade info
            DF keys:
                # 'delta_T_cascade' - delta T of temperature intervals
                # 'mcp_cascade'
                # 'dH'

        # df_operating - DF with stream operating and its characteristics
             DF keys:
                # 'Fluid' - fluid type
                # 'Flowrate'  [kg/h]]
                # 'Supply_Temperature'  [ºC]
                # 'Target_Temperature'  [ºC]
                # 'Cp'  [kJ/kg.K]
                # 'mcp'  [kJ/K]
                # 'Stream_Type' - hot or cold
                # 'Supply_Shift'  [ºC]
                # 'Target_Shift'  [ºC]

##############################
RETURN:
        # 'delta_T_cascade' - delta T of temperature intervals
        # 'mcp_cascade'
        # 'dH'

"""

import numpy as np

def pinch_point(df_heat_cascade,df_operating):

    heat_sum = 0
    minimum = 0
    net_heat_flow = [heat_sum]

    for index, temperature_interval in df_heat_cascade[::-1].iterrows():

        heat_sum += temperature_interval["dH"] *10**(-3) #MJ/h
        net_heat_flow.append(heat_sum)

        # Get Pinch Point, where heat sum cascade is minimum
        if heat_sum < minimum:
            minimum = heat_sum

    # Add heat in pinch point to new heat flow
    net_heat_flow = np.add(net_heat_flow, [abs(minimum)]*len(net_heat_flow))

    # vector wih unique temperatures sorted
    temperature_vector = np.unique(np.append(df_operating["Supply_Shift"].values, df_operating["Target_Shift"].values))[::-1]

    pinch_point_T = temperature_vector[net_heat_flow == 0]
    pinch_point_T = pinch_point_T[0]

    return pinch_point_T