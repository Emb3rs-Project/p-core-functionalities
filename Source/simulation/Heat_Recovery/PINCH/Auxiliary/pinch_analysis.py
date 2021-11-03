"""

INFO: Perform Pinch Analysis

Return: DF with HX
        ['Power' [kW], 'Hot_Stream' [index], 'Cold_Stream' [index], 'Type'  [hx type], 'Turnkey_Cost'  [€],
        'OM_Fix_Cost'  [€/year], 'Hot_Stream_T_Hot'  [ºC], 'Hot_Stream_T_Cold'  [ºC],
        'Original_Hot_Stream' [index], 'Original_Cold_Stream ' [index], 'Storage'  [m3],
        'Storage_Satisfies' [%], 'Storage_Turnkey_Cost'  [€],
        'Total_Turnkey_Cost'  [€], 'Recovered_Energy'  [kWh]]


"""



import pandas as pd
from Source.simulation.Heat_Recovery.PINCH.Auxiliary.table_heat_cascade import table_heat_cascade
from Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_point import pinch_point
from Source.simulation.Heat_Recovery.PINCH.Auxiliary.plot_gcc import plot_gcc
from Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_main import above_pinch_main
from Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_main import below_pinch_main
import numpy as np
from Source.simulation.Heat_Recovery.PINCH.HX.hx_storage import hx_storage

def pinch_analysis(df_operating,df_profile,delta_T_min):

    # Eliminate Solid Flows
    index_eliminate = df_operating[df_operating['Fluid'] == 'solid']
    df_operating.drop(index_eliminate.index, inplace=True)

    # HEAT CASCADE
    df_heat_cascade = table_heat_cascade(df_operating)

    # PINCH POINT
    pinch_point_T, net_heat_flow = pinch_point(df_heat_cascade)

    # PLOT GCC
    temperature_vector = np.unique(np.append(df_operating["Supply_Shift"].values, df_operating["Target_Shift"].values))[
                         ::-1]  # vector wih unique temperatures sorted
    plot_gcc(net_heat_flow, temperature_vector)

    # PINCH ANALYSIS -------------------------------------------
    pinch_point_T = temperature_vector[net_heat_flow == 0]
    pinch_point_T = pinch_point_T[0]

    # Create DF HX
    df_operating['Original_Stream'] = df_operating.index
    df_hx = pd.DataFrame(columns=['Power',
                                  'Hot_Stream',
                                  'Cold_Stream',
                                  'Type',
                                  'HX_Turnkey_Cost',
                                  'OM_Fix_Cost',
                                  'Hot_Stream_T_Hot',
                                  'Hot_Stream_T_Cold',
                                  'Original_Hot_Stream',
                                  'Original_Cold_Stream',
                                  'Storage'])

    # Above Pinch
    df_hx_above_pinch = above_pinch_main(df_operating, delta_T_min, pinch_point_T, df_hx)  # get df with HX
    df_hx_above_pinch = hx_storage(df_profile, df_hx_above_pinch)  # update df with HX storage
    # Below Pinch
    df_hx_below_pinch = below_pinch_main(df_operating, delta_T_min, pinch_point_T, df_hx)
    df_hx_below_pinch = hx_storage(df_profile, df_hx_below_pinch)


    # OUTPUT
    df_hx = pd.concat([df_hx_above_pinch, df_hx_below_pinch])


    if df_hx.empty == False:
        total_heat = 0
        for index, row in df_operating.iterrows():
            total_heat += df_operating['mcp'][index] * abs(
                df_operating['Supply_Temperature'][index] - df_operating['Target_Temperature'][index])



    return df_hx



