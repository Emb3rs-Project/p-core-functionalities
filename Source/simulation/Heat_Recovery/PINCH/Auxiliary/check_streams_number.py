"""
@author: jmcunha/alisboa

Info: Check if Streams In < Streams Out at pinch point. If not, split largest Stream Out to match largest mcp Stream In.

"""

import pandas as pd
import itertools
import numpy as np


def check_streams_number(df_cold_streams, df_hot_streams, above_pinch):
    # Check if above/below pinch
    if above_pinch == True:
        df_streams_in = df_hot_streams.copy()
        df_streams_out = df_cold_streams.copy()
    else:
        df_streams_in = df_cold_streams.copy()
        df_streams_out = df_hot_streams.copy()

    if df_streams_out.shape[0] < df_streams_in.shape[0]:

        surplus_of_streams = df_streams_in.shape[0] - df_streams_out.shape[0]
        print(surplus_of_streams)
        all_index = []

        # do all possible combinations between the streams
        for index_stream_out in df_streams_out.index.values:
            a = [index_stream_out]
            combo = np.append(index_stream_out, df_streams_in.index.values)
            print(combo)
            all_index.append([list(tup) for tup in itertools.combinations(combo, 2)])

        print(all_index)

        for i in combinations:
            # get copy to create multiple splitting options
            df_streams_in_copy = df_streams_in.copy()
            df_streams_out_copy = df_streams_out.copy()

            # Init Vars
            no_repeat_df_streams_in_index = []  # vector to append id not to be repeated
            no_repeat_df_streams_out_index = []
            no_repeat_df_streams_in = pd.Index([])  # empty id transformer
            no_repeat_df_streams_out = pd.Index([])

            # Get rows of both DFs with max mcp
            while df_streams_out.shape[0] < df_streams_in.shape[0]:
                # DF Streams In
                find_df_streams_in_index = True
                df = df_streams_in[
                    ~df_streams_in.index.isin(no_repeat_df_streams_in)].copy()  # get DF without streams already chosen
                while find_df_streams_in_index == True:
                    stream_in = df[df['mcp'] == max(df['mcp'].values)].iloc[0]  # get row with max mcp
                    stream_in_index = stream_in.name  # find index of row with max mcp
                    if stream_in_index in no_repeat_df_streams_in:  # check index until find unused stream index.
                        find_df_streams_in_index = True
                    else:
                        find_df_streams_in_index = False

                # DF Streams Out
                find_df_streams_out_index = True
                df = df_streams_out[~df_streams_out.index.isin(no_repeat_df_streams_out)].copy()
                while find_df_streams_out_index == True:
                    stream_out = df[df['mcp'] == max(df['mcp'].values)].iloc[0]
                    stream_out_index = stream_out.name
                    if stream_out_index in no_repeat_df_streams_out:
                        find_df_streams_out_index = True
                    else:
                        find_df_streams_out_index = False

                # Add Split Stream to DF Streams In
                new_row = stream_out
                new_row['mcp'] = stream_out['mcp'] - stream_in['mcp']
                df_streams_out.loc[int(stream_out_index) * 100, :] = new_row  # new ID

                # Update Original Stream
                df_streams_out.loc[stream_out_index, ['mcp']] = stream_in['mcp']

                # Populate with rows not to be chosen
                no_repeat_df_streams_in_index.append(stream_in_index)
                no_repeat_df_streams_in = pd.Index(no_repeat_df_streams_in_index)  # transform in index
                no_repeat_df_streams_out_index.append(stream_out_index)
                no_repeat_df_streams_out = pd.Index(no_repeat_df_streams_out_index)

        if above_pinch == True:
            return df_streams_out, df_streams_in
        else:
            return df_streams_in, df_streams_out
