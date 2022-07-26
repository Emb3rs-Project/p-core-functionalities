import pandas as pd
from ..Above_Pinch.above_pinch_match_remaining_streams import above_pinch_match_remaining_streams
from ..Below_Pinch.below_pinch_match_remaining_streams import below_pinch_match_remaining_streams


def match_remaining_streams_main(kb, df_streams_in, df_streams_out, df_hx, above_pinch, hx_delta_T, restriction):
    """Main function to match remaining streams.

    Matching is done depending on being above/below pinch and if there are restrictions or not. An iterative computation
    was done to design each iteration the most powerful HX. To achieve this, every possible match combination between
    streams available was done and the respective HX designed. At the end, the HX with larger power was chosen and
    df_streams_in and df_streams_out updated ("tick off rule"). The process, then, repeats itself.

    Due to the use of this "ticking of rule" when matching the remaining streams, more complex cases may lead to the
    streams_in not reaching their 'Supply_Temperature' (remember that the matches are designed from the pinch temperature
    outwards). This means no solution of the pinch analysis, since df_streams_in are not satisfied.

    ** "Tick of rule" - heuristic of maximising the heat load on an interchanger by completely satisfying the heat load
    on one stream (Kemp, Pinch Analysis and Process Integration) **

    Parameters
    ----------
    kb : dict
        Knowledge Base Data

    df_streams_in : df
        DF with streams going into the pinch

    df_streams_out : df
        DF with streams going out of the pinch

    df_hx : df
        DF with heat exchangers data

    above_pinch : boolean

    hx_delta_T : float
        Minimum heat exchanger temperature difference

    restriction : boolean
        Consider restrictions (TRUE] or not (FALSE)

    Returns
    -------
    df_streams_in : df
        DF updated

    df_streams_out : df
        DF updated

    df_hx : df
        DF updated

    """

    # check if above/below pinch
    if above_pinch == True:
        df_hot_streams = df_streams_in.copy()
        df_cold_streams = df_streams_out.copy()
    else:
        df_hot_streams = df_streams_out.copy()
        df_cold_streams = df_streams_in.copy()

    # drop streams which are already complete
    if above_pinch == True:
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            if int(round(hot_stream['Closest_Pinch_Temperature'])) == int(round(hot_stream['Supply_Temperature'])):
                df_hot_streams.drop(index=hot_stream_index, inplace=True)

        for cold_stream_index, cold_stream in df_cold_streams.iterrows():
            if int(round(cold_stream['Closest_Pinch_Temperature'])) == int(round(cold_stream['Target_Temperature'])):
                df_cold_streams.drop(index=cold_stream_index, inplace=True)

    else:
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            if int(round(hot_stream['Closest_Pinch_Temperature'])) == int(round(hot_stream['Target_Temperature'])):
                df_hot_streams.drop(index=hot_stream_index, inplace=True)

        for cold_stream_index, cold_stream in df_cold_streams.iterrows():
            if int(round(cold_stream['Closest_Pinch_Temperature'])) == int(round(cold_stream['Supply_Temperature'])):
                df_cold_streams.drop(index=cold_stream_index, inplace=True)

    # create dummy df to only make changes in original df in the end
    if above_pinch == True:
        df_dummy = df_hot_streams.copy()
    else:
        df_dummy = df_cold_streams.copy()

    # get larger power matches
    while df_dummy.shape[0] > 0:

        # create dummy dfs
        df_hot_streams_dummy = df_hot_streams.copy()
        df_cold_streams_dummy = df_cold_streams.copy()

        if (df_hot_streams_dummy.empty == True) or (df_cold_streams_dummy.empty == True):
            break

        df_hx_dummy = pd.DataFrame(columns=df_hx.columns)

        # match all streams
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            for cold_stream_index, cold_stream in df_cold_streams.iterrows():

                # design HX
                if above_pinch == True:
                    x, x, new_generated_hx = above_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream,
                                                                                 cold_stream_index, cold_stream,
                                                                                 df_cold_streams_dummy,
                                                                                 df_hot_streams_dummy,
                                                                                 hx_delta_T, restriction)


                else:
                    x, x, new_generated_hx = below_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream,
                                                                                 cold_stream_index, cold_stream,
                                                                                 df_cold_streams_dummy,
                                                                                 df_hot_streams_dummy,
                                                                                 hx_delta_T, restriction)

                # reset dummy to compute all hx
                df_hot_streams_dummy = df_hot_streams.copy()
                df_cold_streams_dummy = df_cold_streams.copy()

                # save all designed HX
                if new_generated_hx != []:
                    df_hx_dummy = pd.concat([df_hx_dummy, pd.DataFrame([new_generated_hx])], ignore_index=True)

        # No HX Possible - Break Function
        if df_hx_dummy.empty == True:
            break
        # HX possible
        else:
            # get HX with largest power
            row_hx_max_power = df_hx_dummy[df_hx_dummy['HX_Power'] == max(df_hx_dummy['HX_Power'].values)].iloc[0]
            if row_hx_max_power['HX_Power'] < 1:  # safety
                break



            df_hx = pd.concat([df_hx, pd.DataFrame([row_hx_max_power])], ignore_index=True)

            # update original dfs
            hot_stream_index = row_hx_max_power['HX_Hot_Stream']
            cold_stream_index = row_hx_max_power['HX_Cold_Stream']
            hot_stream = df_hot_streams.loc[hot_stream_index]
            cold_stream = df_cold_streams.loc[cold_stream_index]

            if above_pinch == True:
                df_cold_streams, df_hot_streams, x = above_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream,
                                                                                         cold_stream_index,
                                                                                         cold_stream, df_cold_streams,
                                                                                         df_hot_streams, hx_delta_T,
                                                                                         restriction)
            else:
                df_cold_streams, df_hot_streams, x = below_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream,
                                                                                         cold_stream_index,
                                                                                         cold_stream,
                                                                                         df_cold_streams,
                                                                                         df_hot_streams,
                                                                                         hx_delta_T, restriction)

            # update dummy df
            if above_pinch == True:
                df_dummy = df_hot_streams.copy()
            else:
                df_dummy = df_cold_streams.copy()

    # drop streams which are already complete
    if above_pinch == True:
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            if int(round(hot_stream['Closest_Pinch_Temperature'])) == int(round(hot_stream['Supply_Temperature'])):
                df_hot_streams.drop(index=hot_stream_index, inplace=True)

        for cold_stream_index, cold_stream in df_cold_streams.iterrows():
            if int(round(cold_stream['Closest_Pinch_Temperature'])) == int(round(cold_stream['Target_Temperature'])):
                df_cold_streams.drop(index=cold_stream_index, inplace=True)

    else:
        for hot_stream_index, hot_stream in df_hot_streams.iterrows():
            if int(round(hot_stream['Closest_Pinch_Temperature'])) == int(round(hot_stream['Target_Temperature'])):
                df_hot_streams.drop(index=hot_stream_index, inplace=True)

        for cold_stream_index, cold_stream in df_cold_streams.iterrows():
            if int(round(cold_stream['Closest_Pinch_Temperature'])) == int(round(cold_stream['Supply_Temperature'])):
                df_cold_streams.drop(index=cold_stream_index, inplace=True)

    # check if above/below pinch
    if above_pinch == True:
        df_streams_in = df_hot_streams
        df_streams_out = df_cold_streams
    else:
        df_streams_out = df_hot_streams
        df_streams_in = df_cold_streams

    return df_streams_in, df_streams_out, df_hx
