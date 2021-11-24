""""
alisboa/jmcunha

##############################
INFO: Above Pinch Point - Pinch Analysis.
      Divided in 3 steps:
        1) 1st match - streams reaching pinch
        2) 2nd match - streams not yet matched
        3) 3rd match - remaining streams with  pinch analysis rules (concerning mcp_in<mcp_out),
        4) 4th match - remaining streams without restrictions (concerning mcp_in<mcp_out).

    Streams In are only split in the 1st match.
    Streams Out are only split before any match.

##############################
INPUT:
        # df_streams
        # hx_delta_T_min
        # pinch_T
        # df_hx

##############################
RETURN:
        # df_hx

"""

from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.check_streams_number import check_streams_number
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.match_remaining_streams_main import match_remaining_streams_main
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.testing_above_pinch_make_pair import main_above_pinch_make_pair
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.special_case import special_case
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.testing_all_first_match_pinch_combinations import testing_all_first_match_pinch_combinations
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.testing_check_streams_number import testing_check_streams_number


def above_pinch_main(df_streams,hx_delta_T_min,pinch_T,df_hx):

    ################################################################################
    # Init Arrays
    above_pinch = True
    df_hx_original = df_hx.copy()
    all_df_hx = []
    output = []

    # Pinch Point Temperatures
    pinch_T_cold = pinch_T - hx_delta_T_min
    pinch_T_hot = pinch_T + hx_delta_T_min

    #pinch_T_hot = 150
   # pinch_T_cold = 140

    hx_delta_T_min = 20



    # Separate Streams Info
    df_hot_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Hot') & (df_streams["Supply_Temperature"] > pinch_T_hot)]  # df hot streams
    df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (df_streams["Target_Temperature"] > pinch_T_cold)]  # df cold streams

    ################################################################################
    # Run Pinch
    if df_hot_streams.empty == False and df_cold_streams.empty == False :
        # introduce new columns
        df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(lambda x: pinch_T_hot if x['Target_Temperature'] < pinch_T_hot else x['Target_Temperature'], axis=1)
        df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(lambda x: pinch_T_cold if x['Supply_Temperature'] < pinch_T_cold else x['Supply_Temperature'], axis=1)
        df_hot_streams['Reach_Pinch'] = df_hot_streams.apply(lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_hot else False, axis=1)
        df_cold_streams['Reach_Pinch'] = df_cold_streams.apply(lambda x: True if x['Closest_Pinch_Temperature'] == pinch_T_cold else False, axis=1)
        df_hot_streams['Match'] = False
        df_cold_streams['Match'] = False


        # special case pre-treatment of data - when both dfs have same stream number and there is a streams_in with larger mcp than all streams_out
        all_cases_pretreatment = special_case(df_hot_streams, df_cold_streams,above_pinch,hx_delta_T_min)

        # check all_cases_pretreatment
        for case_pretreatment in all_cases_pretreatment:

            # get data
            df_hot_streams, df_cold_streams = case_pretreatment

            # check number_streams_out < number_streams_in; and get all streams combinations possible
            all_cases_check_streams = testing_check_streams_number(df_hot_streams, df_cold_streams, above_pinch, hx_delta_T_min, reach_pinch=True)


            # check all_cases_check_streams
            for case_check_streams in all_cases_check_streams:
                # get data
                df_hot_streams , df_cold_streams= case_check_streams
                print(
                    '????????????????????????????????????????????????????????????????????????')
                print(
                    '????????????????????????????????????????????????????????????????????????????????????????????????????????????')




                # 1ST MATCH - streams reaching pinch
                all_cases_first_match = testing_all_first_match_pinch_combinations(df_hot_streams,df_cold_streams,df_hx,hx_delta_T_min,above_pinch)



            # check all_cases_first_match
            for case_first_match in all_cases_first_match:
                # get data
                df_hot_streams, df_cold_streams, df_hx = case_first_match


                # check again if number_streams_hot < number_streams_cold; and get all streams combinations possible
                all_cases_check_streams_2 = testing_check_streams_number(df_hot_streams, df_cold_streams, above_pinch,
                                                                       hx_delta_T_min, reach_pinch=False)

                # append df with HX to all cases
                for case in all_cases_check_streams_2:
                    case.append(df_hx)

                # check all_cases_check_streams
                for case_check_streams_2 in all_cases_check_streams_2:
                    # get data
                    df_hot_streams, df_cold_streams, df_hx = case_check_streams_2


                    # REMAINING STREAMS MATCH - WITH Restrictions; match by maximum power HX until all in streams_in are satisfied
                    df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams,
                                                                                          df_cold_streams,
                                                                                          df_hx, above_pinch,
                                                                                          hx_delta_T_min,
                                                                                          restriction=True)

                    # REMAINING STREAMS MATCH - NO Restrictions; match by maximum power HX until all in streams_in are satisfied
                    df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams,
                                                                                          df_cold_streams,
                                                                                          df_hx, above_pinch,
                                                                                          hx_delta_T_min,
                                                                                          restriction=False)
                    # append only unique HX
                    if df_hot_streams.shape[0]>1:
                        values_round = df_hot_streams['Closest_Pinch_Temperature'].apply(lambda x: int(round(x)))

                        # get all HX designed for each solution
                        if False not in (df_hot_streams['Supply_Temperature'].values == values_round.values):
                            all_df_hx.append(df_hx)

                    else:
                        values_round = int(round(df_hot_streams['Closest_Pinch_Temperature']))
                        # get all HX designed for each solution
                        if df_hot_streams['Supply_Temperature'].values == values_round:
                            all_df_hx.append(df_hx)

    # check for repeated HX designed

    if all_df_hx != []:

        for i in all_df_hx:
            i.drop(columns=['Hot_Stream', 'Cold_Stream'], inplace=True)
        keep = []

        if len(all_df_hx) > 1:
            keep.append(all_df_hx[0])
            for i in all_df_hx:
                append = True

                for j in keep:
                    if i.equals(j) != True and append == True:
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

    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('ABOVE PINCH')
    print('len',len(output))
    print(output)

    return output
