"""
alisboa/jmcunha

##############################
INFO: Perform Pinch Analysis.
      1) get heat cascade
      2) get pinch point
      3) separate streams into above and below pinch point
      4) perform pinch analysis and design storage (above and below pinch point)


##############################
INPUT:
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

        # df_profile - DF with all streams schedules (hourly schedule with 1 and 0)
        # delta_T_min - heat exchangers minimum delta T [ºC]


##############################
RETURN: DF with HX designed:
            DF keys:
                # 'Power' [kW]
                # 'Type'  [hx type]
                # 'Turnkey_Cost'  [€]
                # 'OM_Fix_Cost'  [€/year]
                # 'Hot_Stream_T_Hot'  [ºC]
                # 'Hot_Stream_T_Cold'  [ºC]
                # 'Original_Hot_Stream'  [index]
                # 'Original_Cold_Stream'  [index]
                # 'Storage'  [m3]
                # 'Storage_Satisfies' [%]
                # 'Storage_Turnkey_Cost'  [€]
                # 'Total_Turnkey_Cost'  [€]
                # 'Recovered_Energy'  [kWh]

"""



import pandas as pd
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.table_heat_cascade import table_heat_cascade
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.pinch_point import pinch_point
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.plot_gcc import plot_gcc
from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_main import above_pinch_main
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_main import below_pinch_main
import numpy as np
from ......Source.simulation.Heat_Recovery.PINCH.HX.hx_storage import hx_storage

def pinch_analysis(df_operating,df_profile,delta_T_min):

    # HEAT CASCADE
    df_heat_cascade = table_heat_cascade(df_operating)

    # PINCH POINT
    pinch_point_temperature = pinch_point(df_heat_cascade,df_operating)

    # PINCH ANALYSIS -------------------------------------------
    # create DF HX
    df_operating['Original_Stream'] = df_operating.index
    df_operating['Match'] = False  # Assign this value in order to match FIRST all available hot streams
    df_hx = pd.DataFrame(columns=['Power',
                                  'Original_Hot_Stream',
                                  'Original_Cold_Stream',
                                  'Hot_Stream_T_Hot',
                                  'Hot_Stream_T_Cold',
                                  'Hot_Stream',
                                  'Cold_Stream',
                                  'HX_Type',
                                  'HX_Turnkey_Cost',
                                  'HX_OM_Fix_Cost',
                                  'Storage'])

    # Above Pinch
    df_hx_above_pinch = above_pinch_main(df_operating, delta_T_min, pinch_point_temperature, df_hx)  # get df with HX
    df_hx_above_pinch = hx_storage(df_profile, df_hx_above_pinch)  # update df with HX storage
    # Below Pinch
    df_hx_below_pinch = below_pinch_main(df_operating, delta_T_min, pinch_point_temperature, df_hx)
    df_hx_below_pinch = hx_storage(df_profile, df_hx_below_pinch)


    # OUTPUT
    df_hx = pd.concat([df_hx_above_pinch, df_hx_below_pinch])

    if df_hx.empty == False:
        total_heat = 0
        for index, row in df_operating.iterrows():
            total_heat += df_operating['mcp'][index] * abs(
                df_operating['Supply_Temperature'][index] - df_operating['Target_Temperature'][index])


    df_hx.drop(['Hot_Stream','Cold_Stream'],axis=1, inplace=True)

    return df_hx



