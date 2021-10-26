"""
@author: jmcunha/alisboa

Info: Main function to match remaining streams. Matching is done depending on being above/below pinch and restrictions.
      Every possible match between streams is done and the respective HX designed. At the end, HX with larger power
      are chosen and DFs are updated.

"""

import pandas as pd
from Source.simulation.Heat_Recovery.Above_Pinch.above_pinch_match_remaining_streams import above_pinch_match_remaining_streams
from Source.simulation.Heat_Recovery.Below_Pinch.below_pinch_match_remaining_streams import below_pinch_match_remaining_streams

def match_remaining_streams_main(df_hot_streams,df_cold_streams,df_hx,above_pinch,delta_T_min,restriction):

    # Check if above/below pinch
    if above_pinch == True:
        # create dummy df to only make changes in original df in the end
        df_dummy = df_hot_streams.copy()
    else:
        df_dummy = df_cold_streams.copy()

    # Get Larger Power Matches
    while df_dummy.shape[0] > 0:

        # Create dummy DFs
        df_hot_streams_dummy = df_hot_streams.copy()
        df_cold_streams_dummy = df_cold_streams.copy()

        if (df_hot_streams_dummy.empty == True) or (df_hot_streams_dummy.empty == True):
            break


        df_hx_dummy = pd.DataFrame(columns=df_hx.columns)

        # Match All Streams
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            for cold_stream_index, cold_stream in df_cold_streams.iterrows():
                # Generate HX
                if above_pinch == True:
                    x, x, new_generated_hx = above_pinch_match_remaining_streams(hot_stream_index, hot_stream, cold_stream_index, cold_stream,
                                                                           df_cold_streams_dummy, df_hot_streams_dummy,
                                                                           delta_T_min, restriction)
                else:
                    x, x, new_generated_hx = below_pinch_match_remaining_streams(hot_stream_index, hot_stream, cold_stream_index, cold_stream,
                                                                           df_cold_streams_dummy, df_hot_streams_dummy,
                                                                           delta_T_min, restriction)
                # Save All Designed HX
                df_hx_dummy = df_hx_dummy.append(new_generated_hx, ignore_index=True)

        # No HX Possible - Break Function
        if df_hx_dummy.empty == True:
            break
        # HX possible
        else:
            # Get HX with Largest Power
            row_hx_max_power = df_hx_dummy[df_hx_dummy['Power'] == max(df_hx_dummy['Power'].values)].iloc[0]

            if row_hx_max_power['Power']<1: # safety
                break

            df_hx = df_hx.append(row_hx_max_power, ignore_index=True)

            # Update DF ORIGINAL
            hot_stream_index = row_hx_max_power['Hot_Stream']
            cold_stream_index = row_hx_max_power['Cold_Stream']
            hot_stream = df_hot_streams.loc[hot_stream_index]
            cold_stream = df_cold_streams.loc[cold_stream_index]

            if above_pinch == True:
                df_cold_streams, df_hot_streams, x = above_pinch_match_remaining_streams(hot_stream_index, hot_stream, cold_stream_index,
                                                                                   cold_stream, df_cold_streams,
                                                                                   df_hot_streams, delta_T_min,
                                                                                               restriction)
            else:
                df_cold_streams, df_hot_streams, x = below_pinch_match_remaining_streams(hot_stream_index, hot_stream, cold_stream_index,
                                                                             cold_stream,
                                                                             df_cold_streams_dummy,
                                                                             df_hot_streams_dummy,
                                                                             delta_T_min, restriction)

            # Update dummy DF
            if above_pinch == True:
                df_dummy = df_hot_streams.copy()
            else:
                df_dummy = df_cold_streams.copy()


    return df_hot_streams,df_cold_streams,df_hx