from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_hx_temperatures import above_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.PINCH.HX.pinch_design_hx import pinch_design_hx
from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_stream_info import above_pinch_stream_info
from copy import deepcopy


def main_above_pinch_make_pair(combination,delta_T_min):

    all_combinations = []
    all_combinations = above_pinch_make_pair(combination,all_combinations,delta_T_min)

    return all_combinations


def above_pinch_make_pair(combination,all_combinations,delta_T_min):
    combination_copy = deepcopy(combination)

    above_pinch = True

    df_hot_streams, df_cold_streams, df_hx = deepcopy(combination_copy.copy())

    df_hot_streams_for_index = df_hot_streams[df_hot_streams['Match'] == False].copy()
    df_cold_streams_for_index = df_cold_streams[df_cold_streams['Match'] == False].copy()

    # get first pair combinations between the streams to increase pinch analysis variability
    for cold_stream_index in df_cold_streams_for_index.index.values:

        save_index_here = deepcopy(-200)

        df_hot_streams, df_cold_streams, df_hx = deepcopy(combination_copy.copy())
        df_hx_copy = df_hx.copy()
        df_cold_streams.loc[cold_stream_index, 'Match'] = False

        save_index = deepcopy(-100)
        for hot_stream_index in df_hot_streams_for_index.index.values:


                if save_index_here != -200:
                    df_cold_streams.loc[save_index_here] = deepcopy((combination_copy[1].loc[save_index_here]).copy())
                    df_cold_streams.loc[save_index_here, 'Match'] = False

                if save_index != -100:
                    df_hot_streams.loc[save_index] = deepcopy((combination_copy[0].loc[save_index]).copy())
                    df_hot_streams.loc[save_index, 'Match'] = False

                df_cold_streams.loc[cold_stream_index, 'Match'] = False
                df_hot_streams.loc[hot_stream_index, 'Match'] = False

                # look for streams_out with larger mcp than streams_in if number_cold_streams = number_hot_streams
                # and for all streams when number_cold_streams < number_hot_streams

                # ORIGINAL IF
               #if (df_cold_streams.loc[cold_stream_index]['mcp'] >= df_hot_streams.loc[hot_stream_index]['mcp'] and df_cold_streams.shape[0] == df_hot_streams.shape[0]):

                if (df_cold_streams.loc[cold_stream_index]['mcp'] >= df_hot_streams.loc[hot_stream_index]['mcp'] and df_cold_streams.shape[0] == df_hot_streams.shape[0]) or (df_cold_streams.loc[cold_stream_index]['mcp'] <= df_hot_streams.loc[hot_stream_index]['mcp'] and df_cold_streams.shape[0] > df_hot_streams.shape[0]):
                    # only relevant to look for streams_out whose temperature can meet streams_in temperature range
                    if (df_cold_streams.loc[cold_stream_index]['Closest_Pinch_Temperature'] + delta_T_min < df_hot_streams.loc[hot_stream_index]['Supply_Temperature'] and above_pinch is True) or ( df_cold_streams.loc[cold_stream_index]['Closest_Pinch_Temperature'] - delta_T_min > df_hot_streams.loc[hot_stream_index]['Supply_Temperature'] and above_pinch is False):

                        if df_cold_streams.loc[cold_stream_index]['Reach_Pinch'] == True and df_hot_streams.loc[hot_stream_index]['Reach_Pinch'] == True:

                            # Hot Stream Max mcp
                            hot_stream = df_hot_streams.loc[hot_stream_index]

                            # Cold Stream closest to Hot Stream mcp
                            cold_stream = df_cold_streams.loc[cold_stream_index]

                            if hot_stream['Match'] == False and cold_stream['Match'] == False:

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
                                    hot_stream_mcp = split_hot_stream_mcp  # update hot stream mcp


                                    new_row = deepcopy(hot_stream.copy())  # split stream has same info as original
                                    new_row['mcp'] -= split_hot_stream_mcp  # correct split mcp
                                    new_row.name = str(int(hot_stream_index) * 100)  # new ID

                                    # Add Split Stream to DFs
                                    df_hot_streams = df_hot_streams.append(new_row)

                                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = above_pinch_hx_temperatures(
                                        hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot,
                                        cold_stream_mcp)

                                    # Update DFs
                                    df_hot_streams.loc[hot_stream_index, ['mcp']] = split_hot_stream_mcp

                                ###############################
                                ###############################

                                # ITS MULTYPLYNG STREAMS

                                ###############################
                                ###############################


                                save_index = deepcopy(hot_stream_index)
                                save_index_here = deepcopy(cold_stream_index)

                                # Update DF ORIGINAL
                                df_cold_streams.loc[cold_stream_index, ['Match']] = True
                                df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_hot
                                df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_hot
                                df_hot_streams.loc[hot_stream_index, ['Match']] = True

                                # Design HX
                                new_hx_row = pinch_design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot, hx_hot_stream_T_cold,
                                                             hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold,
                                                             cold_stream_fluid, hx_power, original_hot_stream_index,
                                                             original_cold_stream_index)



                                df_hx = df_hx.append(new_hx_row, ignore_index=True)
                                combination = [df_hot_streams,df_cold_streams,df_hx]


                                if df_hot_streams[df_hot_streams['Match'] == False].shape[0] > 0:
                                    all_combinations = above_pinch_make_pair(deepcopy(combination.copy()), deepcopy(all_combinations),delta_T_min)
                                else:

                                    df_hx = df_hx.drop_duplicates(subset=['Original_Hot_Stream','Hot_Split'], keep='last',)
                                    df_hx = df_hx.drop_duplicates(subset=['Original_Cold_Stream','Cold_Split'], keep='last',)

                                    df_hx.drop(columns=['Hot_Split','Cold_Split'],inplace=True)
                                    all_combinations.append(deepcopy([df_hot_streams,df_cold_streams,df_hx]))



    return all_combinations



