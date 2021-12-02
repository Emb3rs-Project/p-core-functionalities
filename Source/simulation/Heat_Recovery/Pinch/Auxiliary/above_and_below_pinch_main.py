""""
alisboa/jmcunha


##############################
INFO: In this function are designed various possible combinations of HX match between hot and cold streams, above or
      below the pinch temperature, respecting the pinch rules. Below, in summary the followed pinch analysis procedure.

      Step by step :
        1) check if special cases
        2) check number_streams_out < number_streams_in
        3) perform first match
        4) check number_streams_out < number_streams_in
        5) match remaining streams according to power - without split and respecting mcp_in<mcp_out
        6) match remaining streams according to power - without split

     1)
     2)
     3)
     4)
     5)
     6)







##############################
INPUT:
        # df_streams
        # hx_delta_T
        # pinch_T
        # df_hx


##############################
RETURN:
        # df_hx

"""

from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.match_remaining_streams_main import match_remaining_streams_main
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.special_case import special_case
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.testing_check_streams_number import testing_check_streams_number
from module.Source.simulation.Heat_Recovery.Pinch.Auxiliary.testing_all_first_match_pinch_combinations import testing_all_first_match_pinch_combinations
from copy import deepcopy


def above_and_below_pinch_main(df_streams, pinch_delta_T_min, pinch_T, df_hx, hx_delta_T, above_pinch):

    ################################################################################
    # Init Arrays
    df_hx_original = deepcopy(df_hx.copy())
    all_df_hx = []

    # get cold and hot pinch point temperatures
    pinch_T_cold = pinch_T - pinch_delta_T_min
    pinch_T_hot = pinch_T + pinch_delta_T_min

    # separate streams info
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

        # special case pre-treatment of data - when both dfs have same stream number and there is a streams_in with larger mcp than all streams_out
        all_cases_pretreatment = special_case(df_streams_in, df_streams_out, above_pinch, hx_delta_T)
        # check all_cases_pretreatment
        for case_pretreatment in all_cases_pretreatment:
            # get data
            df_streams_in, df_streams_out = case_pretreatment

            # check number_streams_out < number_streams_in; and get all streams combinations possible
            all_cases_check_streams = testing_check_streams_number(df_streams_in, df_streams_out, above_pinch,
                                                                   hx_delta_T, reach_pinch=True, check_time=1)


            # check all_cases_check_streams
            for case_check_streams in all_cases_check_streams:
                # get data
                df_streams_in, df_streams_out = case_check_streams
                df_hx = df_hx_original.copy()

                # 1ST MATCH - streams reaching pinch
                all_cases_first_match = testing_all_first_match_pinch_combinations(df_streams_in, df_streams_out, df_hx, hx_delta_T, above_pinch)



                # check all_cases_first_match
                for case_first_match in all_cases_first_match:
                    # get data
                    df_streams_in, df_streams_out, df_hx = case_first_match

                     # check again if number_streams_hot < number_streams_cold; and get all streams combinations possible
                    all_cases_check_streams_2 = testing_check_streams_number(df_streams_in, df_streams_out, above_pinch,hx_delta_T, reach_pinch=False, check_time=2)

                    # append df with HX to all cases
                    for case in all_cases_check_streams_2:
                        case.append(df_hx)

                    # check all_cases_check_streams
                    for case_check_streams_2 in all_cases_check_streams_2:
                        # get data
                        df_streams_in, df_streams_out, df_hx = case_check_streams_2


                        # REMAINING STREAMS MATCH - WITH Restrictions; match by maximum power HX until all in streams_in are satisfied
                        df_streams_in, df_streams_out, df_hx = match_remaining_streams_main(df_streams_in,
                                                                                              df_streams_out,
                                                                                              df_hx, above_pinch,
                                                                                              hx_delta_T,
                                                                                              restriction=True)



                        # REMAINING STREAMS MATCH - NO Restrictions; match by maximum power HX until all in streams_in are satisfied
                        df_streams_in, df_streams_out, df_hx = match_remaining_streams_main(df_streams_in,
                                                                                              df_streams_out,
                                                                                              df_hx, above_pinch,
                                                                                              hx_delta_T,
                                                                                              restriction=False)


                        # append HX designed if all streams in reach pinch
                        if df_streams_in.empty:

                            utility = 0
                            for index, row in df_streams_out.iterrows():
                                utility += row['mcp'] * abs(row['Closest_Pinch_Temperature'] - row['Target_Temperature'])

                            all_df_hx.append({'df_hx': df_hx ,
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

            output = keep

        else:
            output = all_df_hx
    else:
        output = []

    return output, pinch_analysis_possible

