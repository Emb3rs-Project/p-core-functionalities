

def make_pairs(combinations, above_pinch,delta_T_min):

    combinations_updated = []
    pairs = []

    for combination in combinations:
        df_streams_out, df_streams_in = combination

        # get first pair combinations between the streams to increase pinch analysis variability
        for index_stream_out in df_streams_out.index.values:
            for index_stream_in in df_streams_in.index.values:
                if df_streams_out.loc[index_stream_out]['Split_Check'] == False and df_streams_in.loc[index_stream_in]['Split_Check'] == False:
                    # only relevant to look for streams_out with larger mcp than streams_in
                    if df_streams_out.loc[index_stream_out]['mcp'] > df_streams_in.loc[index_stream_in]['mcp']:
                        # only relevant to look for streams_out whose temperature can meet streams_in temperature range
                        if (df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature'] + delta_T_min <
                            df_streams_in.loc[index_stream_in][
                                'Supply_Temperature'] and above_pinch is True) or (
                                df_streams_out.loc[index_stream_out][
                                    'Closest_Pinch_Temperature'] - delta_T_min >
                                df_streams_in.loc[index_stream_in][
                                    'Supply_Temperature'] and above_pinch is False):
                            pairs += [[index_stream_out, index_stream_in]]


        for pair in pairs:

            index_stream_out, index_stream_in = pair

            if above_pinch == True:

                hx_cold_stream_T_cold = df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature']
                hot_stream_max_T_hot = df_streams_in.loc[index_stream_in]['Supply_Temperature']
                cold_stream_max_T_hot = df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature']
                cold_stream_mcp = df_streams_out.loc[index_stream_out]['mcp']
                hot_stream_T_cold = df_streams_out.loc[index_stream_in]['Closest_Pinch_Temperature']
                hot_stream = df_streams_out.loc[index_stream_in]
                hot_stream_index = index_stream_in

                # Compute/Check Temperatures
                if hot_stream_max_T_hot >= (cold_stream_max_T_hot + delta_T_min):
                    hx_cold_stream_T_hot = cold_stream_max_T_hot
                else:
                    hx_cold_stream_T_hot = hot_stream_max_T_hot - delta_T_min

                hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
                hx_hot_stream_T_hot = hot_stream_max_T_hot
                hx_hot_stream_T_cold = hot_stream_T_cold

                # Create Split Stream
                split_hot_stream_mcp = hx_power / (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

                new_row = hot_stream.copy()  # split stream has same info as original
                new_row['mcp'] -= split_hot_stream_mcp  # correct split mcp
                new_row.name = str(int(hot_stream_index) * 100)  # new ID
                new_row['Split_Check'] = False

                # Add Split Stream to DFs
                df_streams_in = df_streams_in.append(new_row)

                # Update DFs
                df_streams_in.loc[index_stream_in]['Split_Check'] = True
                df_streams_in.loc[hot_stream_index, ['mcp']] = split_hot_stream_mcp

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


            combinations_updated.append([df_streams_out, df_streams_in])


    return combinations_updated