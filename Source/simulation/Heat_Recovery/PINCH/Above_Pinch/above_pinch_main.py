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
from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_first_match import above_pinch_first_match
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.testing_above_pinch_make_pair import main_above_pinch_make_pair
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.pretreatment import pretreatment

import numpy as np

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

   # pinch_T_cold = 500
    #pinch_T_hot = 550
    hx_delta_T_min = 20
    #hx_delta_T_min = 50

    # Separate Streams Info
    df_hot_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Hot') & (df_streams["Supply_Temperature"] > pinch_T_hot)] # df hot streams
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
        df_hot_streams['Completed'] = False
        df_cold_streams['Completed'] = False


        # special case pre-treatment of data - when both dfs have same stream number and there is a streams_in with larger mcp than all streams_out
        all_cases_pretreatment = pretreatment(df_hot_streams, df_cold_streams,above_pinch,hx_delta_T_min)

        # check all_cases_pretreatment
        for case_pretreatment in all_cases_pretreatment:
            # get data
            df_hot_streams, df_cold_streams = case_pretreatment

            # check number_streams_hot < number_streams_cold; and get all streams combinations possible
            all_cases_check_streams = check_streams_number(df_cold_streams,df_hot_streams,above_pinch,hx_delta_T_min,reach_pinch=True)  # array with arrays with [df_hot,df_cold]

            # check all_cases_check_streams
            for case_check_streams in all_cases_check_streams:
                print('-------------------------------')
                print('-------------------------------')

                # get data
                df_cold_streams, df_hot_streams = case_check_streams

                # 1ST MATCH - streams reaching pinch
                case_check_streams = [df_hot_streams, df_cold_streams, df_hx_original]

                # get all combinations first match reaching pinch
                all_cases_first_match = main_above_pinch_make_pair(case_check_streams , hx_delta_T_min)


                ############## MAYBE ELIMINATE THIS ? OUR PUT IT INSIDE THE FUNCTION BEFORE ######################
                keep = []
                if len(all_cases_first_match) > 1:
                    keep.append(all_cases_first_match[0])
                    for case_all_cases_first_match in all_cases_first_match:
                        append = True
                        for index , case_keep in enumerate(keep):

                            case_keep[2] = case_keep[2].sort_values('HX_Turnkey_Cost')
                            case_all_cases_first_match[2] = case_all_cases_first_match[2].sort_values('HX_Turnkey_Cost')

                            case_keep[2].index = np.arange(1 , len(case_keep[2]) + 1)
                            case_all_cases_first_match[2].index = np.arange(1 , len(case_all_cases_first_match[2]) + 1)

                            if (case_keep[2].drop(columns=['Hot_Stream' , 'Cold_Stream'])).equals(
                                    case_all_cases_first_match[2].drop(
                                            columns=['Hot_Stream' , 'Cold_Stream'])) != True and append == True:
                                append = True
                            else:
                                append = False

                        if append == True:
                            keep.append(case_all_cases_first_match)

                else:
                    keep = all_cases_first_match
                ############## MAYBE ELIMINATE THIS ? OUR PUT IT INSIDE THE FUNCTION BEFORE ######################



                # matches and streams to keep
                all_cases_first_match = keep.copy()
            else:
                pass

            # check all_cases_first_match
            for case_first_match in all_cases_first_match:

                df_hot_streams, df_cold_streams, df_hx = case_first_match

                # check again if number_streams_hot < number_streams_cold; and get all streams combinations possible
                all_cases_check_streams_2 = check_streams_number(df_cold_streams , df_hot_streams , above_pinch ,hx_delta_T_min,reach_pinch=False)  # array with arrays with [df_hot,df_cold]

                print(all_cases_check_streams_2)

                for i in all_cases_check_streams_2:
                    i.append(df_hx)


                # check all_cases_first_match

                for case_check_streams_2 in all_cases_check_streams_2:
                    # get data
                    df_hot_streams , df_cold_streams , df_hx = case_check_streams_2


                    # REMAINING STREAMS MATCH - WITH Restrictions; match by maximum power HX until all in streams_in are satisfied
                    restriction = True
                    df_hot_streams , df_cold_streams , df_hx = match_remaining_streams_main(df_hot_streams ,
                                                                                            df_cold_streams ,
                                                                                            df_hx , above_pinch ,
                                                                                            hx_delta_T_min ,
                                                                                            restriction)

                    # REMAINING STREAMS MATCH - NO Restrictions; match by maximum power HX until all in streams_in are satisfied
                    restriction = False
                    df_hot_streams , df_cold_streams , df_hx = match_remaining_streams_main(df_hot_streams ,
                                                                                            df_cold_streams ,
                                                                                            df_hx , above_pinch ,
                                                                                            hx_delta_T_min ,
                                                                                            restriction)

                    # get all HX designed for each solution
                    all_df_hx.append(df_hx)


    # check for repeated HX designed
    if all_df_hx != []:

                for i in all_df_hx:
                    i.drop(columns=['Hot_Stream' , 'Cold_Stream'] , inplace=True)
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
                    output.append(all_df_hx)


    else:
        output = []


    print('####################################################')
    print('####################################################')

    print('output')

    for i in output:
        print(i[['Power', 'Original_Hot_Stream','Original_Cold_Stream']])

    print('####################################################')
    print('####################################################')

    output = output[0]

    return output