

def special_case(df_hot_streams, df_cold_streams, above_pinch,delta_T_min):

    # initial value
    split_needed = False
    pairs = []
    combinations_updated = []

    # check if abvoe or below pinch
    if above_pinch == True:
        df_streams_in = df_hot_streams.copy()
        df_streams_out = df_cold_streams.copy()
    else:
        df_streams_in = df_cold_streams.copy()
        df_streams_out = df_hot_streams.copy()

    # only perform this split when both df's have same stream number and there is a streams_in with larger mcp than all streams_out
    if df_streams_in.shape[0] == df_streams_out.shape[0] :

        # check if there is a stream in larger than all streams out
        index_streams_in_to_split = []
        for index,row in df_streams_in.iterrows():


            if False in df_streams_out.apply(lambda x: True if x['mcp'] < row['mcp'] else False, axis=1).values:
                pass
            else:
                split_needed = True
                index_streams_in_to_split.append(index)

        if split_needed == True:
            # get first pair combinations between the streams to increase pinch analysis variability
            for index_stream_out in df_streams_out.index.values:
                for index_stream_in in index_streams_in_to_split:
                    # only relevant to look for streams_out with larger mcp than streams_in
                    if df_streams_in.loc[index_stream_in]['mcp'] > df_streams_out.loc[index_stream_out]['mcp']:
                        # only relevant to look for streams_out whose temperature can meet streams_in temperature range
                        if (df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature'] + delta_T_min < df_streams_in.loc[index_stream_in]['Supply_Temperature'] and above_pinch is True) or (  df_streams_out.loc[index_stream_out][ 'Closest_Pinch_Temperature'] - delta_T_min >  df_streams_in.loc[index_stream_in]['Supply_Temperature'] and above_pinch is False):
                            pairs += [[index_stream_out, index_stream_in]]

            for pair in pairs:
                df_streams_in_copy = df_streams_in.copy()
                df_streams_out_copy = df_streams_out.copy()
                index_stream_out, index_stream_in = pair

                if above_pinch == True:

                    hot_stream_index = index_stream_in
                    cold_stream_index = index_stream_out

                    hx_cold_stream_T_cold = df_streams_out_copy.loc[index_stream_out]['Closest_Pinch_Temperature']
                    cold_stream_max_T_hot = df_streams_out_copy.loc[index_stream_out]['Target_Temperature']
                    cold_stream_mcp = df_streams_out_copy.loc[index_stream_out]['mcp']
                    cold_stream = df_streams_out_copy.loc[index_stream_out]
                    hot_stream = df_streams_in_copy.loc[index_stream_in]

                    hot_stream_max_T_hot = df_streams_in_copy.loc[index_stream_in]['Supply_Temperature']
                    hot_stream_T_cold = df_streams_in_copy.loc[index_stream_in]['Closest_Pinch_Temperature']
                    hot_stream_mcp = df_streams_in_copy.loc[index_stream_in]['mcp']

                    # Compute/Check Temperatures
                    if hot_stream_max_T_hot >= (cold_stream_max_T_hot + delta_T_min):
                        hx_cold_stream_T_hot = cold_stream_max_T_hot
                    else:
                        hx_cold_stream_T_hot = hot_stream_max_T_hot - delta_T_min

                    # Split Stream in
                    hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
                    hx_hot_stream_T_hot = hot_stream_max_T_hot
                    hx_hot_stream_T_cold = hot_stream_T_cold

                    # Create Split Stream
                    split_hot_stream_mcp = hx_power / (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

                    new_row = hot_stream.copy()  # split stream has same info as original
                    new_row['mcp'] -= split_hot_stream_mcp  # correct split mcp
                    new_row.name = str(int(hot_stream_index) * 100)  # new ID

                    new_row['Split_Check'] = True

                    # Add Split Stream to DFs
                    df_streams_in_copy = df_streams_in_copy.append(new_row)

                    # Update DFs
                    df_streams_in_copy.loc[hot_stream_index, ['Split_Check']] = True
                    df_streams_in_copy.loc[hot_stream_index, ['mcp']] = split_hot_stream_mcp

                else:

                    cold_stream_min_T_cold = df_streams_in.loc[index_stream_in]['Supply_Temperature']
                    hot_stream_min_T_cold = df_streams_out.loc[index_stream_out]['Target_Temperature']
                    hot_stream_T_hot = df_streams_out.loc[index_stream_out]['Supply_Temperature']
                    hot_stream_mcp = df_streams_out.loc[index_stream_out]['mcp']
                    cold_stream_T_hot = df_streams_in.loc[index_stream_in]['Closest_Pinch_Temperature']
                    cold_stream = df_streams_in.loc[index_stream_in]
                    cold_stream_index = index_stream_in

                    # Compute/Check Temperatures
                    if cold_stream_min_T_cold <= (hot_stream_min_T_cold - delta_T_min):
                        hot_stream_T_cold = hot_stream_min_T_cold
                    else:
                        hot_stream_T_cold = cold_stream_min_T_cold + delta_T_min

                    hx_power = hot_stream_mcp * (hot_stream_T_hot - hot_stream_T_cold)
                    cold_stream_T_cold = cold_stream_min_T_cold

                    # Create Split Stream
                    split_stream_mcp = hx_power / (cold_stream_T_hot - cold_stream_T_cold)

                    new_row = cold_stream.copy()  # split stream has same info
                    new_row['mcp'] -= split_stream_mcp  # correct mcp
                    new_row.name = str(int(cold_stream_index) * 100)  # new ID
                    new_row['Split_Check'] = False

                    # Add Split Stream to DFs
                    df_streams_in = df_streams_in.append(new_row)

                    # Update DFs
                    df_streams_in.loc[index_stream_in]['Split_Check'] = True
                    df_streams_in.loc[cold_stream_index, ['mcp']] = split_stream_mcp

                combinations_updated.append([df_streams_in_copy, df_streams_out_copy])

            all_combinations = combinations_updated

        else:
            all_combinations = [[df_hot_streams ,df_cold_streams]]


    else:
        all_combinations = [[df_hot_streams, df_cold_streams]]

    return all_combinations