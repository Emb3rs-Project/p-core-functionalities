""""
alisboa/jmcunha

##############################
INFO: Get pinch point.
      Find theoretical minimum heat and cold utilities.


##############################
INPUT:
        # df_heat_cascade
        # df_operating - DF with stream operating and its characteristics

            Where in df_heat_cascade, the following keys:
                # delta_T_cascade - temperature intervals on the heat cascade
                # mcp_cascade  [kJ/K]
                # dH - enthalpy computed for each temperature interval  [kJ]

            Where in df_operating, the following keys:
                # Fluid - fluid type
                # Flowrate  [kg/h]
                # Supply_Temperature  [ºC]
                # Target_Temperature  [ºC]
                # Cp  [kJ/kg.K]
                # mcp  [kW/K]
                # Stream_Type - hot or cold
                # Supply_Shift  [ºC]
                # Target_Shift  [ºC]


##############################
RETURN:
        # pinch_point_T  [ºC]
        # theo_minimum_hot_utility - minimum theoretical hot utility  [kW]
        # theo_minimum_cold_utility - minimum theoretical cold utility  [kW]

"""

import numpy as np

def pinch_point(df_heat_cascade, df_operating):
    """Get pinch point

    Find theoretical minimum heat and cold utilities.

    Parameters
    ----------
    df_heat_cascade : df
        DF with the heat cascade data

    df_operating : df
        DF with streams operating and its characteristics

    Returns
    -------
    pinch_point_T : float
        [ºC]

    theo_minimum_hot_utility : float
        Minimum theoretical hot utility [kW]

    theo_minimum_cold_utility : float
        Minimum theoretical cold utility [kW]


    """

    heat_sum = 0
    minimum = 0
    net_heat_flow = [heat_sum]

    for index, temperature_interval in df_heat_cascade[::-1].iterrows():

        heat_sum += temperature_interval["dH"]  # [kW]
        net_heat_flow.append(heat_sum)

        # minimum in heat cascade sum is where it lies the pinch temperature
        if heat_sum < minimum:
            minimum = heat_sum

    # add heat needed at pinch point to the net heat flow
    net_heat_flow = np.add(net_heat_flow, [abs(minimum)] * len(net_heat_flow))

    # vector wih unique temperatures sorted
    temperature_vector = np.unique(np.append(df_operating["Supply_Shift"].values, df_operating["Target_Shift"].values))[
                         ::-1]
    pinch_point_T = temperature_vector[net_heat_flow == 0][0]

    # get minimum theoretical hot/cold utility for the streams analyzed
    if net_heat_flow[0] == 0:
        theo_minimum_hot_utility = 0 # [kW]
        theo_minimum_cold_utility = net_heat_flow[-1]
    else:
        theo_minimum_hot_utility = net_heat_flow[0]
        theo_minimum_cold_utility = net_heat_flow[-1]

    return pinch_point_T, theo_minimum_hot_utility, theo_minimum_cold_utility
