""""
jmcunha/alisboa

Info: Below Pinch Point Analysis. Divided in 3 steps: 1st match streams reaching pinch, 2nd match remaining streams with
pinch analysis rules (concerning mcp_in<mcp_out), 3rd match remaining streams without restrictions. Streams Out are only
split before matching  and Streams In are only split in 1st match.

"""

from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.check_streams_number import check_streams_number
from ......Source.simulation.Heat_Recovery.PINCH.Auxiliary.match_remaining_streams_main import match_remaining_streams_main
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_first_match import below_pinch_first_match

def below_pinch_main(df_streams, delta_T_min, pinch_T, df_hx):

    # Init Arrays
    above_pinch = False

    # Pinch Point Temperatures
    pinch_T_cold = pinch_T - delta_T_min
    pinch_T_hot = pinch_T + delta_T_min

    # Separate Streams Info
    df_hot_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Hot') & (df_streams["Target_Temperature"] < pinch_T_hot)]
    df_cold_streams = df_streams.copy()[(df_streams["Stream_Type"] == 'Cold') & (df_streams["Supply_Temperature"] < pinch_T_cold)]

    if df_cold_streams.empty == False:
        # Get Streams Closest Temperature to Pinch Point
        df_hot_streams['Closest_Pinch_Temperature'] = df_hot_streams.apply(lambda x: pinch_T_hot if x['Supply_Temperature'] > pinch_T_hot else x['Supply_Temperature'], axis=1)
        df_cold_streams['Closest_Pinch_Temperature'] = df_cold_streams.apply(lambda x: pinch_T_cold if x['Target_Temperature'] > pinch_T_cold else x['Target_Temperature'], axis=1)


        # Check N_streams COLD < N_streams HOT
        all_cases = check_streams_number(df_cold_streams, df_hot_streams, above_pinch,delta_T_min) # array with arrays with [df_cold, df_hot]


        # 1ST MATCH - Streams Reaching Pinch ----------------------------------------------------------
        df_hot_streams_dummy = df_hot_streams[df_hot_streams['Closest_Pinch_Temperature'] == pinch_T_hot].copy()
        df_cold_streams_dummy = df_cold_streams[df_cold_streams['Closest_Pinch_Temperature'] == pinch_T_cold].copy()

        df_hot_streams, df_cold_streams, df_hx = below_pinch_first_match(df_hot_streams, df_cold_streams, df_hot_streams_dummy, df_cold_streams_dummy, df_hx, delta_T_min)

        # REMAINING 1ST MATCH -   ----------------------------------------------------------
        df_cold_streams_dummy =  df_cold_streams[df_cold_streams['Match'] == False].copy()

        while df_cold_streams_dummy.shape[0] > 0:
            df_cold_streams_dummy = df_cold_streams_dummy[df_cold_streams_dummy['mcp'] == max(df_cold_streams_dummy['mcp'].values)]
            df_hot_streams_dummy = df_hot_streams[(df_hot_streams['Closest_Pinch_Temperature'] > df_cold_streams_dummy['Closest_Pinch_Temperature'].values[0]+ delta_T_min)].copy()

            if df_hot_streams_dummy.empty == True:
                break

            df_hot_streams, df_cold_streams,df_hx = below_pinch_first_match(df_hot_streams, df_cold_streams, df_hot_streams_dummy,df_cold_streams_dummy, df_hx, delta_T_min)
            df_cold_streams_dummy = df_cold_streams[df_cold_streams['Match'] == False].copy()

        # REMAINING MATCH - WITH Restrictions  ----------------------------------------------------------
        restriction = True
        df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx, above_pinch, delta_T_min, restriction)


        # REMAINING MATCH - NO Restrictions ----------------------------------------------------------
        restriction = False
        df_hot_streams, df_cold_streams, df_hx = match_remaining_streams_main(df_hot_streams, df_cold_streams, df_hx, above_pinch, delta_T_min, restriction)


    return df_hx