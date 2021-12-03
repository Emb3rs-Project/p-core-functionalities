""""
alisboa/jmcunha


##############################
INFO: In this function are designed various possible combinations of HX match between hot and cold streams, above or
      below the pinch temperature, respecting the pinch rules. The pinch rules being, number of streams_out at pinch
      equal/larger than streams_in and when matching streams, the mcp of the stream_out has to be equal/larger than
      stream_in mcp (this rule is not only applied at the step 6, see below). To try to solve majority of cases and also
      give different design solutions, at special_case/testing_check_streams_number/
      testing_all_first_match_pinch_combinations, all the possible combinations of streams are done. Even though it can
      be time consuming when a large number of streams is given, it has an added benefit of proposing more pinch designs.

      The pinch analysis can be a complex decision/design analysis according to the streams given, thus it was
      implemented a code structure that is thought to best perform in the majority of cases.

      Summary of the Pinch analysis chain of thought step by step :
        1) data treatment
        1) check if special cases (** special_case)
        2) check number_streams_out < number_streams_in (** testing_check_streams_number)
        3) perform first match (** testing_all_first_match_pinch_combinations)
        4) check number_streams_out < number_streams_in (** testing_check_streams_number)
        5) match remaining streams according to power - without split and respecting mcp_in<mcp_out (** match_remaining_streams_main)
        6) match remaining streams according to power - without split (** match_remaining_streams_main)

     ** detailed information about each function in its script **


##############################
INPUT:
        # df_streams
        # pinch_delta_T_min - delta temperature for pinch analysis  [ºC]
        # pinch_T  [ºC]
        # hx_delta_T - heat exchangers minimum delta T  [ºC]
        # above_pinch  [True or False]

        Where in df_streams, the necessary following keys:
            # Fluid - fluid type
            # Flowrate  [kg/h]
            # Supply_Temperature  [ºC]
            # Target_Temperature  [ºC]
            # mcp  [kW/K]
            # Stream_Type - hot or cold
            # Supply_Shift  [ºC]
            # Target_Shift  [ºC]


##############################
RETURN:
        # all_designs - array with different hx design (df_hx)  possibilities
        # pinch_analysis_possible - check if it was possible to perform pinch analysis above/below pinch [True or False]

        Where in each df_hx of all_designs, the following keys:
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


"""

from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.match_remaining_streams_main import match_remaining_streams_main
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.special_cases import special_cases
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.testing_check_streams_number import testing_check_streams_number
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.testing_all_first_match_pinch_combinations import testing_all_first_match_pinch_combinations
from copy import deepcopy
import pandas as pd

def above_and_below_pinch_main(df_streams, pinch_delta_T_min, pinch_T, hx_delta_T, above_pinch):

    ################################################################################
    # Init Arrays
    all_df_hx = []

    # get hot/cold pinch point temperatures
    pinch_T_cold = pinch_T - pinch_delta_T_min
    pinch_T_hot = pinch_T + pinch_delta_T_min

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

    df_hx_original = deepcopy(df_hx.copy())

    # separate streams info
    df_streams['Original_Stream'] = df_streams.index
    df_streams['Match'] = False
    df_streams['Split'] = False

    if above_pinch == True:
        df_hot_streams = df_streams.copy()[
            (df_streams["Stream_Type"] == 'Hot') & (df_streams["Supply_Temperature"] > pinch_T_hot)]
        df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (
                    df_streams["Target_Temperature"] > pinch_T_cold)]
    else:
        df_hot_streams = df_streams.copy()[
            (df_streams["Stream_Type"] == 'Hot') & (df_streams["Target_Temperature"] < pinch_T_hot)]
        df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (
                    df_streams["Supply_Temperature"] < pinch_T_cold)]  #


    ################################################################################
    # Data Treatment
    # 1) get streams closest temperature to pinch
    # 2) know if streams reach pinch
    # 3) define streams_in and streams_out

    if df_hot_streams.empty is False and df_cold_streams.empty is False:
        pinch_analysis_possible = True

        if above_pinch == True:
            df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(
                lambda x: pinch_T_hot if x['Target_Temperature'] < pinch_T_hot else x['Target_Temperature'], axis=1)
            df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(
                lambda x: pinch_T_cold if x['Supply_Temperature'] < pinch_T_cold else x['Supply_Temperature'], axis=1)
            df_hot_streams['Reach_Pinch'] = df_hot_streams.apply(
                lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_hot else False, axis=1)
            df_cold_streams['Reach_Pinch'] = df_cold_streams.apply(
                lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_cold else False, axis=1)

            df_streams_in = df_hot_streams
            df_streams_out = df_cold_streams

        else:
            df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(
                lambda x: pinch_T_hot if x['Supply_Temperature'] > pinch_T_hot else x['Supply_Temperature'], axis=1)
            df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(
                lambda x: pinch_T_cold if x['Target_Temperature'] > pinch_T_cold else x['Target_Temperature'], axis=1)
            df_hot_streams['Reach_Pinch'] = df_hot_streams.apply(
                lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_hot else False, axis=1)
            df_cold_streams['Reach_Pinch'] = df_cold_streams.apply(
                lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_cold else False, axis=1)

            df_streams_in = df_cold_streams
            df_streams_out = df_hot_streams


        ########################################################################################################
        # Run Pinch
        # 1) check if special cases
        # 2) check number_streams_out < number_streams_in
        # 3) perform first match
        # 4) check number_streams_out < number_streams_in
        # 5) match remaining streams according to power - without split and respecting mcp_in<mcp_out
        # 6) match remaining streams according to power - without split

        # special case
        all_cases_pretreatment = special_cases(df_streams_in, df_streams_out, above_pinch, hx_delta_T)

        # check all_cases_pretreatment
        for case_pretreatment in all_cases_pretreatment:
            df_streams_in, df_streams_out = case_pretreatment

            # check number_streams_out < number_streams_in
            all_cases_check_streams = testing_check_streams_number(df_streams_in, df_streams_out, above_pinch,
                                                                   hx_delta_T, reach_pinch=True, check_time=1)

            # check all_cases_check_streams
            for case_check_streams in all_cases_check_streams:
                df_streams_in, df_streams_out = case_check_streams
                df_hx = df_hx_original.copy()

                # 1ST MATCH - streams reaching pinch
                all_cases_first_match = testing_all_first_match_pinch_combinations(df_streams_in, df_streams_out, df_hx,
                                                                                   hx_delta_T, above_pinch)

                # check all_cases_first_match
                for case_first_match in all_cases_first_match:
                    df_streams_in, df_streams_out, df_hx = case_first_match

                    # check if number_streams_hot < number_streams_cold
                    all_cases_check_streams_2 = testing_check_streams_number(df_streams_in, df_streams_out, above_pinch,
                                                                             hx_delta_T, reach_pinch=False,
                                                                             check_time=2)

                    # append df with HX to all cases
                    for case in all_cases_check_streams_2:
                        case.append(df_hx)

                    # check all_cases_check_streams
                    for case_check_streams_2 in all_cases_check_streams_2:
                        df_streams_in, df_streams_out, df_hx = case_check_streams_2

                        # REMAINING STREAMS MATCH - WITH Restrictions
                        df_streams_in, df_streams_out, df_hx = match_remaining_streams_main(df_streams_in,
                                                                                            df_streams_out,
                                                                                            df_hx, above_pinch,
                                                                                            hx_delta_T,
                                                                                            restriction=True)

                        # REMAINING STREAMS MATCH - NO Restrictions
                        df_streams_in, df_streams_out, df_hx = match_remaining_streams_main(df_streams_in,
                                                                                              df_streams_out,
                                                                                              df_hx, above_pinch,
                                                                                              hx_delta_T,
                                                                                              restriction=False)

                        # append HX designed if all streams_in reach pinch
                        if df_streams_in.empty:
                            utility = 0
                            for index, row in df_streams_out.iterrows():
                                utility += row['mcp'] * abs(row['Closest_Pinch_Temperature'] - row['Target_Temperature'])

                            all_df_hx.append({'df_hx': df_hx,
                                              'utility': utility,
                                              })

    else:
        pinch_analysis_possible = False


    ########################################################################################################
    # OUTPUT

    # check for repeated HX designed
    if all_df_hx != []:
        for i in all_df_hx:
            i['df_hx'].drop(columns=['Hot_Stream', 'Cold_Stream'], inplace=True)
        keep = []
        if len(all_df_hx) > 1:
            keep.append(all_df_hx[0])
            for i in all_df_hx:
                i_df_hx = i['df_hx'].sort_values(by=['HX_Turnkey_Cost'])
                append = True

                for j in keep:
                    j_df_hx = j['df_hx'].sort_values(by=['HX_Turnkey_Cost'])

                    if i_df_hx[['Power', 'Original_Stream_In', 'Original_Stream_Out', 'HX_Turnkey_Cost']].equals(
                            j_df_hx[['Power', 'Original_Stream_In', 'Original_Stream_Out',
                                     'HX_Turnkey_Cost']]) != True and append == True:
                        append = True
                    else:
                        append = False

                if append == True:
                    keep.append(i)

            all_designs = keep

        else:
            all_designs = all_df_hx
    else:
        all_designs = []

    return all_designs, pinch_analysis_possible

