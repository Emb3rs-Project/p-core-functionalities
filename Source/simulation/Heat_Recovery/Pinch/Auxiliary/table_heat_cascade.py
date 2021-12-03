""""
alisboa/jmcunha

##############################
INFO: Compute heat cascade. The heat cascade is a net enthalpy heat balance which allow us to compute the minimum
      hot and cold utility, as well as the pinch point.


##############################
INPUT:
        # df_operating - DF with the characteristics of operating streams

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
        # df_heat_cascade - info necessary to compute pinch point

            Where in df_heat_cascade, the following keys:
                # delta_T_cascade - temperature intervals on the heat cascade
                # mcp_cascade  [kW/K]
                # dH - enthalpy computed for each temperature interval  [kW]

"""

import pandas as pd
import numpy as np


def table_heat_cascade(df_operating):

    # vector wih unique temperatures sorted
    temperature_vector = np.unique(np.append(df_operating["Supply_Shift"].values, df_operating["Target_Shift"].values))

    # get mcp for each temperature interval
    delta_T_cascade = []
    mcp_cascade = []
    for i in range(1, len(temperature_vector)):
        delta_T_cascade.append(temperature_vector[i] - temperature_vector[i - 1])
        mcp = 0

        # check all streams in the considered delta_T
        for index, stream in df_operating.iterrows():
            if stream["Stream_Type"] == 'Hot':
                if temperature_vector[i - 1] >= stream['Target_Shift'] and \
                        temperature_vector[i] <= stream["Supply_Shift"]:
                    mcp += stream['mcp']
            else:
                if temperature_vector[i - 1] >= stream['Supply_Shift'] and \
                        temperature_vector[i] <= stream["Target_Shift"]:
                    mcp += - stream['mcp']

        mcp_cascade.append(mcp)

    # create heat cascade DF
    df_heat_cascade = pd.DataFrame({"delta_T_cascade": delta_T_cascade,
                                    "mcp_cascade": mcp_cascade},
                                   index=pd.IntervalIndex.from_breaks(temperature_vector)
                                   )

    df_heat_cascade['dH'] = df_heat_cascade['delta_T_cascade'] * df_heat_cascade['mcp_cascade']

    return df_heat_cascade
