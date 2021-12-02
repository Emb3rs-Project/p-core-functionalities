"""
alisboa/jmcunha

##############################
INFO: Perform Pinch Analysis.
      Step by step:
          1) compute heat cascade
          2) get pinch point
          3) separate streams into above and below pinch point
          4) perform pinch analysis and design storage (above and below pinch point)
          5) make combinations between above and below designs
          6) create clean output with detailed information regarding each option

      Important:
        - Very specific/complex cases may not be solved, sending an empty output.


##############################
INPUT:
        # df_profile - DF with all streams schedules (hourly schedule with 1 and 0)
        # pinch_delta_T_min - delta temperature for pinch analysis divided by 2 [ºC]
        # hx_delta_T - heat exchangers minimum delta T [ºC]
        # design_id  [ID]
        # df_operating - DF with stream operating and its characteristics

             Where in df_operating, the following keys:
                # Fluid - fluid type
                # Flowrate  [kg/h]]
                # Supply_Temperature  [ºC]
                # Target_Temperature  [ºC]
                # Cp  [kJ/kg.K]
                # mcp  [kJ/K]
                # Stream_Type - hot or cold
                # Supply_Shift  [ºC]
                # Target_Shift  [ºC]


##############################
RETURN: list with the cases designed as dictionaries

            Each one provides the following keys:
                # ID - design ID [ID]
                # analysis_state - shows message: 'error in performing - probably specific/complex case' or 'performed'
                # streams - streams ID  [ID]
                # theo_minimum_hot_utility - minimum theoretical hot utility  [kW]
                # hot_utility  [kW]
                # theo_minimum_cold_utility - minimum theoretical cold utility  [kW]
                # cold_utility  [kW]
                # pinch_temperature  [ºC]
                # df_hx  [kg CO2/kWh]

                Where in df_hx, the following keys:
                    # Power  [kW]
                    # HX_Hot_Stream  [ID]
                    # HX_Cold_Stream  [ID]
                    # HX_Original_Hot_Stream  [ID]
                    # HX_Original_Cold_Stream  [ID]
                    # HX_Type  [hx type]
                    # HX_Turnkey_Cost  [€]
                    # HX_OM_Fix_Cost  [€/year]
                    # HX_Hot_Stream_T_Hot  [ºC]
                    # HX_Hot_Stream_T_Cold  [ºC]
                    # HX_Cold_Stream_T_Hot  [ºC]
                    # HX_Cold_Stream_T_Cold  [ºC]
                    # Storage  [m3]
                    # Storage_Satisfies  [%]
                    # Storage_Turnkey_Cost  [€]
                    # Total_Turnkey_Cost  [€]
                    # Recovered_Energy  [kWh/year]

"""


import pandas as pd
from ......Source.simulation.Heat_Recovery.Pinch.Auxiliary.table_heat_cascade import table_heat_cascade
from ......Source.simulation.Heat_Recovery.Pinch.Auxiliary.pinch_point import pinch_point
from ......Source.simulation.Heat_Recovery.Pinch.Auxiliary.plot_gcc import plot_gcc
from ......Source.simulation.Heat_Recovery.Pinch.Below_Pinch.above_and_below_pinch_main import above_and_below_pinch_main
from ......Source.simulation.Heat_Recovery.Pinch.HX.hx_storage import hx_storage

def pinch_analysis(df_operating,df_profile,pinch_delta_T_min,hx_delta_T,design_id):

    # data treatment
    df_operating['Original_Stream'] = df_operating.index
    df_operating['Match'] = False
    df_operating['Split'] = False

    # get heat cascade
    df_heat_cascade = table_heat_cascade(df_operating)

    # get pinch point
    pinch_point_temperature, minimum_hot_utility, minimum_cold_utility = pinch_point(df_heat_cascade, df_operating)

    # create DF for heat exchangers
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


    ############################################################################################################
    # PINCH
    # Above Pinch - get HXs and respective storage
    info_df_hx_above_pinch, above_pinch_analysis_possible = above_and_below_pinch_main(df_operating,
                                                                                       pinch_delta_T_min,
                                                                                       pinch_point_temperature,
                                                                                       df_hx,
                                                                                       hx_delta_T,
                                                                                       above_pinch=True)
    info_df_hx_above_pinch = hx_storage(df_profile,
                                        info_df_hx_above_pinch,
                                        above_pinch=True)

    # Below Pinch - get HXs and respective storage
    info_df_hx_below_pinch, below_pinch_analysis_possible = above_and_below_pinch_main(df_operating,
                                                                                       pinch_delta_T_min,
                                                                                       pinch_point_temperature,
                                                                                       df_hx,
                                                                                       hx_delta_T,
                                                                                       above_pinch=False)
    info_df_hx_below_pinch = hx_storage(df_profile,
                                        info_df_hx_below_pinch,
                                        above_pinch=False)

    # make df_hx combinations - with above and below designs
    vector_df_hx = []

    # cases where is only possible to do above pinch analysis
    if len(info_df_hx_above_pinch) > 0 and len(info_df_hx_below_pinch) > 0:
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

    # cases where is only possible to do below pinch analysis
    elif len(info_df_hx_above_pinch) == 0 and len(
            info_df_hx_below_pinch) > 0 and above_pinch_analysis_possible == False:
        for df_hx_below in info_df_hx_below_pinch:
            cold_utility = df_hx_below['utility']
            df_hx_below = df_hx_below['df_hx']
            vector_df_hx.append({
                'df_hx': df_hx_below,
                'hot_utility': minimum_hot_utility,
                'cold_utility': cold_utility})

    # cases where is only possible to do above pinch analysis
    elif len(info_df_hx_above_pinch) > 0 and len(
            info_df_hx_below_pinch) == 0 and below_pinch_analysis_possible == False:
        for df_hx_above in info_df_hx_above_pinch:
            hot_utility = df_hx_above['utility']
            df_hx_above = df_hx_above['df_hx']
            vector_df_hx.append({
                'df_hx': df_hx_above,
                'hot_utility': hot_utility,
                'cold_utility': minimum_cold_utility})


    ############################################################################################################
    # OUTPUT
    detailed_info_pinch_analysis = []

    if len(vector_df_hx) > 0:
        for df_hx in vector_df_hx:
            detailed_info_pinch_analysis.append({'ID': design_id,
                                                 'analysis_state': 'performed',
                                                 'streams': df_operating.index.values,
                                                 'theo_minimum_hot_utility': minimum_hot_utility,
                                                 'hot_utility': df_hx['hot_utility'],
                                                 'theo_minimum_cold_utility': minimum_cold_utility,
                                                 'cold_utility': df_hx['cold_utility'],
                                                 'df_hx': df_hx['df_hx'],
                                                 'pinch_temperature': pinch_point_temperature
                                                 })

            design_id += 1

    else:
        # very specific/complex cases may not be solved
        detailed_info_pinch_analysis.append({'ID': design_id,
                                             'analysis_state': 'error in performing - probably specific/complex case',
                                             'streams': df_operating.index.values,
                                             'theo_minimum_hot_utility': minimum_hot_utility,
                                             'hot_utility': None,
                                             'theo_minimum_cold_utility': minimum_cold_utility,
                                             'cold_utility': None,
                                             'df_hx': None,
                                             'pinch_temperature': pinch_point_temperature
                                             })
        design_id += 1


    return detailed_info_pinch_analysis,design_id



