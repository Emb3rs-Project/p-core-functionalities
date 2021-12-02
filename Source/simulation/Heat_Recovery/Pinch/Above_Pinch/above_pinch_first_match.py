from ......Source.simulation.Heat_Recovery.Pinch.Above_Pinch.above_pinch_hx_temperatures import above_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.Pinch.HX.pinch_design_hx import pinch_design_hx
from ......Source.simulation.Heat_Recovery.Pinch.Above_Pinch.above_pinch_stream_info import above_pinch_stream_info

def above_pinch_first_match(combinations, df_hot_streams, df_cold_streams, df_hot_streams_dummy, df_cold_streams_dummy, df_hx, delta_T_min):

    combinations = [1]

    for combination in combinations:

        while df_hot_streams_dummy.shape[0] > 0:

            if df_cold_streams_dummy.empty == True:
                break

            # Hot Stream Max mcp
            hot_stream = df_hot_streams_dummy[df_hot_streams_dummy['mcp'] == max(df_hot_streams_dummy['mcp'].values)].iloc[0]
            hot_stream_index = hot_stream.name # get index

            # Cold Stream closest to Hot Stream mcp
            cold_stream_index = df_cold_streams_dummy.first_valid_index()  # random initial index
            cold_stream = df_cold_streams_dummy.loc[cold_stream_index]
            dif = abs(hot_stream['mcp'] - df_cold_streams_dummy.loc[cold_stream_index]['mcp'])

            for index, row in df_cold_streams_dummy.iterrows():
                dif_new = abs(hot_stream['mcp'] - row['mcp'])
                if (dif_new < dif) or (dif_new == dif and row['mcp'] > cold_stream['mcp']):  # prefer higher mcp
                    dif = dif_new
                    cold_stream_index = index
                    cold_stream = df_cold_streams_dummy.loc[cold_stream_index]

            # Streams Info
            hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_T_cold, cold_stream_max_T_hot, cold_stream_mcp, cold_stream_fluid, original_hot_stream_index, original_cold_stream_index = above_pinch_stream_info(hot_stream, cold_stream)


            # NO SPLIT
            if hot_stream_mcp <= cold_stream_mcp:
                # Compute HX Temperatures
                hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = above_pinch_hx_temperatures(
                    hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot,
                    cold_stream_mcp)

            # SPLIT
            else:
                hx_cold_stream_T_cold = cold_stream_T_cold

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
                hot_stream_mcp = split_hot_stream_mcp # update hot stream mcp

                new_row = hot_stream.copy()  # split stream has same info as original
                new_row['mcp'] -= split_hot_stream_mcp  # correct split mcp
                new_row.name = str(int(hot_stream_index) * 100)  # new ID

                # Add Split Stream to DFs
                df_hot_streams_dummy = df_hot_streams_dummy.append(new_row)
                df_hot_streams = df_hot_streams.append(new_row)

                hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = above_pinch_hx_temperatures(
                    hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot,
                    cold_stream_mcp)

                # Update DFs
                df_hot_streams.loc[hot_stream_index, ['mcp']] = split_hot_stream_mcp


            # 1st MATCH DONE - Drop Streams of DF PINCH
            df_cold_streams_dummy.drop(index=cold_stream_index, inplace=True)
            df_hot_streams_dummy.drop(index=hot_stream_index, inplace=True)

            # Update DF ORIGINAL
            df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_hot
            df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_hot
            df_hot_streams.loc[hot_stream_index, ['Match']] = True



            # Design HX
            new_hx_row = pinch_design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot, hx_hot_stream_T_cold,
                                             hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold,
                                             cold_stream_fluid, hx_power,original_hot_stream_index,original_cold_stream_index)

            df_hx = df_hx.append(new_hx_row, ignore_index=True)

            # Drop fulfilled streams DF ORIGINAL
            if df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']].values == df_hot_streams.loc[hot_stream_index, ['Supply_Temperature']].values:
                    df_hot_streams.drop(index=hot_stream_index, inplace=True)
            if df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']].values == df_cold_streams.loc[
                    cold_stream_index, ['Target_Temperature']].values:
                    df_cold_streams.drop(index=cold_stream_index, inplace=True)


    return df_hot_streams, df_cold_streams, df_hx