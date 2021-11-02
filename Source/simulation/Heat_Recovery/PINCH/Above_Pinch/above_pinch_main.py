""""
jmcunha/alisboa

Info: Above Pinch Point Analysis. Divided in 3 steps: 1st match - streams reaching pinch, 2nd match - streams not yet matched, 3rd match - remaining streams with
pinch analysis rules (concerning mcp_in<mcp_out), 4th match - remaining streams without restrictions (concerning mcp_in<mcp_out).
Streams In are only split in 1st match.
Streams Out are only split before any match.

"""

from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.check_streams_number import check_streams_number
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.match_remaining_streams_main import match_remaining_streams_main
from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_first_match import above_pinch_first_match


def above_pinch_main(df_streams,delta_T_min,T_pinch,df_hx):
    # Init Arrays
    above_pinch = True

    # Pinch Point Temperatures
    T_pinch_cold = T_pinch - delta_T_min
    T_pinch_hot = T_pinch + delta_T_min


    # Separate Streams Info
    df_hot_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Hot') & (df_streams["Supply_Temperature"] > T_pinch_hot)] # df hot streams
    df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (df_streams["Target_Temperature"] > T_pinch_cold)]  # df cold streams
    df_hot_streams['Match'] = False # Assign this value in order to match FIRST all available hot streams


    if df_hot_streams.empty == False :

        # Get Streams Closest Temperature to Pinch Point
        df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(lambda x: T_pinch_hot if x['Target_Temperature'] < T_pinch_hot else x['Target_Temperature'], axis=1)
        df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(lambda x: T_pinch_cold if x['Supply_Temperature'] < T_pinch_cold else x['Supply_Temperature'], axis=1)


        # Check N_streams HOT < N_streams COLD
        df_cold_streams, df_hot_streams = check_streams_number(df_cold_streams, df_hot_streams,above_pinch)

        # 1ST MATCH - Streams Reaching Pinch ----------------------------------------------------------
        df_hot_streams_dummy = df_hot_streams[df_hot_streams['Closest_Pinch_Temperature'] == T_pinch_hot].copy()
        df_cold_streams_dummy = df_cold_streams[df_cold_streams['Closest_Pinch_Temperature'] == T_pinch_cold].copy()
        df_hot_streams,df_cold_streams,df_hx = above_pinch_first_match(df_hot_streams, df_cold_streams, df_hot_streams_dummy, df_cold_streams_dummy, df_hx, delta_T_min)


        # REMAINING 1ST MATCH - Attention to temperatures  ----------------------------------------------------------
        df_hot_streams_dummy = df_hot_streams[df_hot_streams['Match'] == False].copy()

        while df_hot_streams_dummy.shape[0] > 0:

            df_hot_streams_dummy = df_hot_streams_dummy[df_hot_streams_dummy['mcp'] == max(df_hot_streams_dummy['mcp'].values)]
            df_cold_streams_dummy = df_cold_streams[(df_cold_streams['Closest_Pinch_Temperature'] + delta_T_min < df_hot_streams_dummy['Closest_Pinch_Temperature'].values[0])].copy()

            if df_cold_streams_dummy.empty == True:
                break

            df_hot_streams, df_cold_streams,df_hx = above_pinch_first_match(df_hot_streams, df_cold_streams, df_hot_streams_dummy,df_cold_streams_dummy, df_hx, delta_T_min)

            df_hot_streams_dummy = df_hot_streams[df_hot_streams['Match'] == False].copy()



        # REMAINING STREAMS MATCH - WITH Restrictions  ----------------------------------------------------------
        restriction = True
        df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx,above_pinch, delta_T_min, restriction)

        # REMAINING STREAMS MATCH - NO Restrictions ----------------------------------------------------------
        restriction = False
        df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx, above_pinch, delta_T_min, restriction)

    return df_hx