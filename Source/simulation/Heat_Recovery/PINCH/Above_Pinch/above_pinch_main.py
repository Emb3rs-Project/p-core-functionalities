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
        # delta_T_min
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

def above_pinch_main(df_streams,delta_T_min,pinch_T,df_hx):

    # Init Arrays
    above_pinch = True

    # Pinch Point Temperatures
    pinch_T_cold = pinch_T - delta_T_min
    pinch_T_hot = pinch_T + delta_T_min

    #pinch_T_cold =90
    #pinch_T_hot = 100
    #delta_T_min = 10

    # Separate Streams Info
    df_hot_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Hot') & (df_streams["Supply_Temperature"] > pinch_T_hot)] # df hot streams
    df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (df_streams["Target_Temperature"] > pinch_T_cold)]  # df cold streams

    if df_hot_streams.empty == False :

        # Get Streams Closest Temperature to Pinch Point
        df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(lambda x: pinch_T_hot if x['Target_Temperature'] < pinch_T_hot else x['Target_Temperature'], axis=1)
        df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(lambda x: pinch_T_cold if x['Supply_Temperature'] < pinch_T_cold else x['Supply_Temperature'], axis=1)

        # Check N_streams HOT < N_streams COLD
        all_cases_check_streams = check_streams_number(df_cold_streams, df_hot_streams,above_pinch,delta_T_min)  # array with arrays with [df_hot,df_cold]

        print('############################################')
        print('############################################')
        print('############################################')

        for case_check_streams in all_cases_check_streams:


            ### CHECK THIS - VERY IMPORTANT
            df_cold_streams, df_hot_streams = case_check_streams

            # 1ST MATCH - Streams Reaching Pinch ----------------------------------------------------------
            df_hot_streams['Reach_Pinch'] = df_hot_streams.apply(lambda x:True if x['Closest_Pinch_Temperature'] == pinch_T_hot else False, axis=1)
            df_cold_streams['Reach_Pinch'] = df_cold_streams.apply(lambda x:True if x['Closest_Pinch_Temperature'] == pinch_T_cold else False, axis=1)

            case_check_streams = [df_hot_streams, df_cold_streams, df_hx]
            ################# UPDATING #################
            combinations = [1]

            try:
                all_cases_first_match = main_above_pinch_make_pair(case_check_streams,delta_T_min)

                keep = []
                if len(all_cases_first_match) > 1:
                    keep.append(all_cases_first_match[0])

                    for case_all_cases_first_match in all_cases_first_match:

                        for case_keep in keep:

                            df = case_all_cases_first_match[2].merge(case_keep[2], how='inner', indicator=False)

                            if df.shape[0] != case_keep[2].shape[0]:
                                keep.append(case_all_cases_first_match)

                all_cases_first_match = keep.copy()
                print('look')
                print(all_cases_first_match)
            except:
                pass

            df_hot_streams_dummy = df_hot_streams[df_hot_streams['Closest_Pinch_Temperature'] == pinch_T_hot].copy()
            df_cold_streams_dummy = df_cold_streams[df_cold_streams['Closest_Pinch_Temperature'] == pinch_T_cold].copy()
            df_hot_streams, df_cold_streams, df_hx = above_pinch_first_match(combinations,df_hot_streams, df_cold_streams, df_hot_streams_dummy, df_cold_streams_dummy, df_hx, delta_T_min)

            all_cases_first_match = [[df_hot_streams, df_cold_streams, df_hx]]
            ################# UPDATING #################

            # REMAINING 1ST MATCH  ----------------------------------------------------------
            for case_first_match in all_cases_first_match:
                df_hot_streams, df_cold_streams, df_hx = case_first_match
                df_hot_streams_dummy = df_hot_streams[df_hot_streams['Match'] == False].copy()

                while df_hot_streams_dummy.shape[0] > 0:
                    df_hot_streams_dummy = df_hot_streams_dummy[df_hot_streams_dummy['mcp'] == max(df_hot_streams_dummy['mcp'].values)]
                    df_cold_streams_dummy = df_cold_streams[(df_cold_streams['Closest_Pinch_Temperature'] + delta_T_min < df_hot_streams_dummy['Closest_Pinch_Temperature'].values[0])].copy()

                    if df_cold_streams_dummy.empty == True:
                        break

                    df_hot_streams, df_cold_streams,df_hx = above_pinch_first_match(combinations,df_hot_streams, df_cold_streams, df_hot_streams_dummy,df_cold_streams_dummy, df_hx, delta_T_min)
                    df_hot_streams_dummy = df_hot_streams[df_hot_streams['Match'] == False].copy()


                # REMAINING STREAMS MATCH - WITH Restrictions  ----------------------------------------------------------
                restriction = True
                df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx,above_pinch, delta_T_min, restriction)

                # REMAINING STREAMS MATCH - NO Restrictions ----------------------------------------------------------
                restriction = False
                df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx, above_pinch, delta_T_min, restriction)

    return df_hx