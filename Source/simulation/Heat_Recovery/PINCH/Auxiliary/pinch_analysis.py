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

def pinch_analysis(df_operating,df_profile,pinch_delta_T_min,hx_delta_T,design_id):

    # HEAT CASCADE
    df_heat_cascade = table_heat_cascade(df_operating)



    # PINCH POINT
    pinch_point_temperature, minimum_hot_utility, minimum_cold_utility = pinch_point(df_heat_cascade,df_operating)

    # PINCH ANALYSIS -------------------------------------------
    # create DF HX
    df_operating['Original_Stream'] = df_operating.index
    df_operating['Match'] = False  # Assign this value in order to match FIRST all available hot streams
    df_operating['Split'] = False
    df_hx = pd.DataFrame(columns=['Power',
                                  'Original_Stream_In',
                                  'Original_Stream_Out',
                                  'Hot_Stream_T_Hot',
                                  'Hot_Stream_T_Cold',
                                  'Hot_Stream',
                                  'Cold_Stream',
                                  'HX_Type',
                                  'HX_Turnkey_Cost',
                                  'HX_OM_Fix_Cost',
                                  'Storage'])

    # Above Pinch
    info_df_hx_above_pinch = above_and_below_pinch_main(df_operating, pinch_delta_T_min, pinch_point_temperature, df_hx,hx_delta_T,above_pinch=True)  # get df with HX

    info_df_hx_above_pinch = hx_storage(df_profile, info_df_hx_above_pinch,above_pinch=True)  # update df with HX storage


    # Below Pinch
    info_df_hx_below_pinch = above_and_below_pinch_main(df_operating, pinch_delta_T_min, pinch_point_temperature, df_hx,hx_delta_T,above_pinch=False)  # get df with HX
    info_df_hx_below_pinch = hx_storage(df_profile, info_df_hx_below_pinch,above_pinch=False)

    # OUTPUT
    # make df_hx combinations - above and below
    vector_df_hx = []

    if len(info_df_hx_above_pinch)>0 and len(info_df_hx_below_pinch)>0:
        for df_hx_above in info_df_hx_above_pinch:
            hot_utility = df_hx_above['utility']
            df_hx_above = df_hx_above['df_hx']
            for df_hx_below in info_df_hx_below_pinch:
                cold_utility = df_hx_below['utility']
                df_hx_below = df_hx_below['df_hx']
                vector_df_hx.append({
                    'df_hx': pd.concat([df_hx_above, df_hx_below], ignore_index=True),
                    'hot_utility': hot_utility,
                    'cold_utility': cold_utility})

    elif len(info_df_hx_above_pinch) == 0 and len(info_df_hx_below_pinch) > 0:
        for df_hx_below in info_df_hx_below_pinch:
            cold_utility = df_hx_below['utility']
            df_hx_below = df_hx_below['df_hx']
            vector_df_hx.append({
                'df_hx': df_hx_below,
                'hot_utility': minimum_hot_utility,
                'cold_utility': cold_utility})

    elif len(info_df_hx_above_pinch) > 0 and len(info_df_hx_below_pinch) == 0:
        for df_hx_above in info_df_hx_above_pinch:
            hot_utility = df_hx_above['utility']
            df_hx_above = df_hx_above['df_hx']
            vector_df_hx.append({
                'df_hx': df_hx_above,
                'hot_utility': hot_utility,
                'cold_utility': minimum_cold_utility})


    detailed_info_pinch_analysis = []

    for df_hx in vector_df_hx:

        detailed_info_pinch_analysis.append({'ID': design_id,
                                            'streams': df_operating.index.values,
                                            'theo_minimum_hot_utility': minimum_hot_utility,
                                            'hot_utility': df_hx['hot_utility'],
                                            'theo_minimum_cold_utility': minimum_cold_utility,
                                            'cold_utility': df_hx['cold_utility'],
                                            'df_hx': df_hx['df_hx'],
                                            'pinch_temperature': pinch_point_temperature
                                        })

        design_id += 1


    print('output ########################################################################################################################')
    for i in vector_df_hx:
        print(i['df_hx'][['Power','Original_Stream_In','Original_Stream_Out','HX_Turnkey_Cost']])



    return detailed_info_pinch_analysis,design_id



