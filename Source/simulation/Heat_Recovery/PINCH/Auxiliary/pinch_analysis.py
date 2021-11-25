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
        # pinch_delta_T_min - heat exchangers minimum delta T [ºC]


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
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.above_and_below_pinch_main import above_and_below_pinch_main
import numpy as np
from ......Source.simulation.Heat_Recovery.PINCH.HX.hx_storage import hx_storage

def pinch_analysis(df_operating,df_profile,pinch_delta_T_min,hx_delta_T):


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
    vector_df_hx_above_pinch = above_and_below_pinch_main(df_operating, pinch_delta_T_min, pinch_point_temperature, df_hx,hx_delta_T,above_pinch=True)  # get df with HX
    vector_df_hx_above_pinch = hx_storage(df_profile, vector_df_hx_above_pinch)  # update df with HX storage

    # Below Pinch
    vector_df_hx_below_pinch = above_and_below_pinch_main(df_operating, pinch_delta_T_min, pinch_point_temperature, df_hx,hx_delta_T,above_pinch=False)  # get df with HX
    vector_df_hx_below_pinch = hx_storage(df_profile, vector_df_hx_below_pinch)

    # OUTPUT
    # make df_hx combinations - above and below
    vector_df_hx = []

    if len(vector_df_hx_above_pinch)>0 and len(vector_df_hx_below_pinch)>0:
        for df_hx_above in vector_df_hx_above_pinch:
            for df_hx_below in vector_df_hx_below_pinch:
                vector_df_hx.append(pd.concat([df_hx_above, df_hx_below],ignore_index=True))

    elif len(vector_df_hx_above_pinch) == 0 and len(vector_df_hx_below_pinch) > 0:
        vector_df_hx = vector_df_hx_below_pinch

    elif len(vector_df_hx_above_pinch) > 0 and len(vector_df_hx_below_pinch) == 0:
        vector_df_hx = vector_df_hx_above_pinch



    return vector_df_hx



