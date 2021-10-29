""""
jmcunha/alisboa

Info: Compute heat cascade.

"""

import pandas as pd
import numpy as np

def table_heat_cascade (df_operating):

    # Vector wih unique temperatures sorted
    temperature_vector = np.unique(np.append(df_operating["Supply_Shift"].values,
                                             df_operating["Target_Shift"].values)
                                   )

    delta_T_cascade = []
    mcp_cascade = []

    for i in range(1, len(temperature_vector)):
        delta_T_cascade.append(temperature_vector[i] - temperature_vector[i - 1])
        mcp = 0

        # Check all streams in the considered delta_T
        for index, stream in df_operating.iterrows():
            if stream["Stream_Type"] == 'Hot':
                if temperature_vector[i - 1] >= stream['Target_Shift'] and temperature_vector[i] <= stream["Supply_Shift"]:
                    mcp += stream['mcp']
            else:
                if temperature_vector[i - 1] >= stream['Supply_Shift'] and temperature_vector[i] <= stream["Target_Shift"]:
                    mcp += - stream['mcp']
        mcp_cascade.append(mcp)


    # Create DF
    df_heat_cascade = pd.DataFrame({"delta_T_cascade": delta_T_cascade, "mcp_cascade": mcp_cascade},
                          index=pd.IntervalIndex.from_breaks(
                              temperature_vector
                          ))

    df_heat_cascade['dH'] = df_heat_cascade['delta_T_cascade'] * df_heat_cascade['mcp_cascade']

    return df_heat_cascade