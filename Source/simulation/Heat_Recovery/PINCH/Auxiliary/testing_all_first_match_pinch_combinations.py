"""
alisboa/jmcunha

##############################
INFO: Make all combinations between streams in and out and design respective HX, to ensure maximum pinch variability.

##############################
INPUT:
        # combination - df_streams_in, df_streams_out, df_hx
        # delta_T_min
        # above_pinch


##############################
RETURN:
        # all_combinations - [df_streams_in, df_streams_out, df_hx]

"""



from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_hx_temperatures import above_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.PINCH.HX.pinch_design_hx import pinch_design_hx
from ......Source.simulation.Heat_Recovery.PINCH.Above_Pinch.above_pinch_stream_info import above_pinch_stream_info
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_stream_info import below_pinch_stream_info
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_hx_temperatures import below_pinch_hx_temperatures

from copy import deepcopy
import numpy as np


def testing_all_first_match_pinch_combinations(df_streams_in, df_streams_out, df_hx, delta_T_min, above_pinch):

    # Init arrays
    all_combinations = []

    # get all combinations with recursive function
    combination = [df_streams_in, df_streams_out, df_hx]


    all_combinations = make_pairs(combination, all_combinations, delta_T_min, above_pinch)

    # eliminate df streams repeated
    if len(all_combinations) > 1:
        keep = [all_combinations[0]]

        for i in all_combinations:
            append = True
            i_copy = i[2].copy()
            i_copy = i_copy.sort_values('HX_Turnkey_Cost')
            i_copy.index = np.arange(1, len(i_copy) + 1)

            for j in keep:
                j_copy = j[2].copy()
                j_copy = j_copy.sort_values('HX_Turnkey_Cost')
                j_copy.index = np.arange(1, len(j_copy) + 1)

                if i_copy[['Power','HX_Turnkey_Cost']].equals(j_copy[['Power','HX_Turnkey_Cost']]) != True and append == True:
                    append = True
                else:
                    append = False

            if append == True:
                keep.append(i)

        all_combinations = keep

    elif len(all_combinations) == 0:
        all_combinations = [combination]

    return all_combinations


def make_pairs(combination, all_combinations, delta_T_min, above_pinch):

    # get streams and hx df's
    combination_copy = deepcopy(combination)

    # get info to make pair matches
    df_streams_in, df_streams_out, df_hx = deepcopy(combination_copy.copy())

    # get streams which were not yet matched
    df_streams_in_for_index = df_streams_in[df_streams_in['Match'] == False].copy()
    df_streams_out_for_index = df_streams_out[df_streams_out['Match'] == False].copy()

    ###############################################################################################
    # Get all combinations between streams to increase pinch analysis variability

    for stream_out_index in df_streams_out_for_index.index.values:
        # save out/in stream random value for iterations
        save_index_out = deepcopy(-200)
        save_index_in = deepcopy(-100)

        # when recursive function goes step back, some values must be restored
        df_streams_in, df_streams_out, df_hx = deepcopy(combination_copy.copy())
        df_streams_out.loc[stream_out_index, 'Match'] = False

        for stream_in_index in df_streams_in_for_index.index.values:
            # when recursive function goes step back, some values must be restored
            if save_index_out != -200:
                # get back stream out
                df_streams_out.loc[save_index_out] = deepcopy((combination_copy[1].loc[save_index_out]).copy())
                df_streams_out.loc[save_index_out, 'Match'] = False

            if save_index_in != -100:
                # get back stream in
                df_streams_in.loc[save_index_in] = deepcopy((combination_copy[0].loc[save_index_in]).copy())
                df_streams_in.loc[save_index_in, 'Match'] = False

            # get back initial value
            df_streams_out.loc[stream_out_index, 'Match'] = False
            df_streams_in.loc[stream_in_index, 'Match'] = False

            ##########################################################################################
            # get streams
            stream_out = df_streams_out.loc[stream_out_index]
            stream_in = df_streams_in.loc[stream_in_index]

            # look for df_streams_out with larger mcp than df_streams_in if number_stream_outs = number_stream_ins
            # and for all streams when number_stream_out > number_stream_in
            if (stream_out['mcp'] >= stream_in['mcp'] and
                df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0] ==
                df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0]) \
                    or (stream_out['mcp'] <= stream_in['mcp'] and
                        df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0] >
                        df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0]) or (stream_out['mcp'] >= stream_in['mcp'] and
                        df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0] >
                        df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0]):

                # only relevant to look for stream_out whose temperature can meet stream_in temperature range
                if (stream_out['Closest_Pinch_Temperature'] + delta_T_min <
                    stream_in['Supply_Temperature'] and above_pinch == True) or (
                        stream_out['Closest_Pinch_Temperature'] - delta_T_min >
                        stream_in['Supply_Temperature'] and above_pinch is False):

                    # only looking to streams which reach pinch
                    if stream_out['Reach_Pinch'] == True and stream_in['Reach_Pinch'] == True:

                        # only looking to streams which were not matched yet
                        if stream_in['Match'] == False and stream_out['Match'] == False:

                            # get streams info
                            if above_pinch == True:
                                stream_in_T_cold, stream_in_max_T_hot, stream_in_mcp, stream_in_fluid, stream_out_T_cold, stream_out_max_T_hot, stream_out_mcp, stream_out_fluid, original_stream_in_index, original_stream_out_index = above_pinch_stream_info(
                                    stream_in, stream_out)
                            else:
                                stream_out_min_T_cold, stream_out_T_hot, stream_out_mcp, stream_out_fluid, stream_in_min_T_cold, stream_in_T_hot, stream_in_mcp, stream_in_fluid, original_stream_out_index, original_stream_in_index = below_pinch_stream_info(
                                    stream_out, stream_in)

                            # NO SPLIT
                            if stream_in_mcp <= stream_out_mcp:
                                # compute HX temperatures
                                if above_pinch == True:
                                    hx_power, hx_stream_in_T_cold, hx_stream_in_T_hot, hx_stream_out_T_cold, hx_stream_out_T_hot = above_pinch_hx_temperatures(
                                        stream_in_T_cold, stream_in_max_T_hot, stream_in_mcp, stream_out_T_cold,
                                        stream_out_max_T_hot,
                                        stream_out_mcp)
                                else:
                                    hx_power, hx_stream_out_T_cold, hx_stream_out_T_hot, hx_stream_in_T_cold, hx_stream_in_T_hot = below_pinch_hx_temperatures(
                                        stream_out_T_hot, stream_out_min_T_cold, stream_out_mcp, stream_in_T_hot,
                                        stream_in_min_T_cold, stream_in_mcp)


                            # SPLIT
                            else:

                                if above_pinch == True:
                                    hx_stream_out_T_cold = stream_out_T_cold

                                    # compute HX temperatures
                                    if stream_in_max_T_hot >= (stream_out_max_T_hot + delta_T_min):
                                        hx_stream_out_T_hot = stream_out_max_T_hot
                                    else:
                                        hx_stream_out_T_hot = stream_in_max_T_hot - delta_T_min

                                    hx_power = stream_out_mcp * (hx_stream_out_T_hot - hx_stream_out_T_cold)
                                    hx_stream_in_T_hot = stream_in_max_T_hot
                                    hx_stream_in_T_cold = stream_in_T_cold

                                    # create split stream
                                    split_stream_in_mcp = hx_power / (hx_stream_in_T_hot - hx_stream_in_T_cold)
                                    stream_in_mcp = split_stream_in_mcp  # update hot stream mcp
                                    new_row = deepcopy(stream_in.copy())  # split stream has same info as original
                                    new_row['mcp'] -= split_stream_in_mcp  # correct split mcp
                                    new_row.name = str(int(stream_in_index) * 100)  # new ID

                                    # Add Split Stream to DFs
                                    df_streams_in = df_streams_in.append(new_row)

                                    hx_power, hx_stream_in_T_cold, hx_stream_in_T_hot, hx_stream_out_T_cold, hx_stream_out_T_hot = above_pinch_hx_temperatures(
                                        stream_in_T_cold, stream_in_max_T_hot, stream_in_mcp, stream_out_T_cold,
                                        stream_out_max_T_hot,
                                        stream_out_mcp)

                                else:
                                    # compute/check temperatures
                                    if stream_in_min_T_cold <= (stream_out_min_T_cold - delta_T_min):
                                        stream_out_T_cold = stream_out_min_T_cold
                                    else:
                                        stream_out_T_cold = stream_in_min_T_cold + delta_T_min

                                    hx_power = stream_out_mcp * (stream_out_T_hot - stream_out_T_cold)
                                    stream_in_T_cold = stream_in_min_T_cold

                                    # create split stream
                                    split_stream_in_mcp = hx_power / (stream_in_T_hot - stream_in_T_cold)
                                    stream_in_mcp = split_stream_in_mcp  # update cold stream mcp
                                    new_row = deepcopy(stream_in.copy())  # split stream has same info as original
                                    new_row['mcp'] -= split_stream_in_mcp  # correct split mcp
                                    new_row.name = str(int(stream_in_index) * 100)  # new ID

                                    # add split stream to df
                                    df_streams_in = df_streams_in.append(new_row)


                                    hx_power, hx_stream_out_T_cold, hx_stream_out_T_hot, hx_stream_in_T_cold, hx_stream_in_T_hot = below_pinch_hx_temperatures(
                                        stream_out_T_hot, stream_out_min_T_cold, stream_out_mcp, stream_in_T_hot,
                                        stream_in_min_T_cold, stream_in_mcp)


                                # update df_streams_in
                                df_streams_in.loc[stream_in_index, ['mcp']] = split_stream_in_mcp

                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_hot
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_hot

                            # save index in case the recursive iteration goes a step back
                            save_index_in = deepcopy(stream_in_index)
                            save_index_out = deepcopy(stream_out_index)

                            # update dfs

                            df_streams_out.loc[stream_out_index, ['Match']] = True
                            df_streams_in.loc[stream_in_index, ['Match']] = True

                            if above_pinch == True:
                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_hot
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_hot
                            else:
                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_cold
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_cold

                            # design HX
                            new_hx_row = pinch_design_hx(stream_in_index, stream_out_index, hx_stream_in_T_hot,
                                                         hx_stream_in_T_cold,
                                                         stream_in_fluid, hx_stream_out_T_hot, hx_stream_out_T_cold,
                                                         stream_out_fluid, hx_power, original_stream_in_index,
                                                         original_stream_out_index)

                            df_hx = df_hx.append(new_hx_row, ignore_index=True)
                            combination = [df_streams_in, df_streams_out, df_hx]

                            # continue iteration or reach end and save
                            if df_streams_in[(df_streams_in['Match'] == False) & (df_streams_in['Reach_Pinch'] == True)].shape[0] > 0:

                                all_combinations = make_pairs(deepcopy(combination.copy()), deepcopy(all_combinations), delta_T_min, above_pinch)

                                # when iteration goes a step back, last HX designed must be eliminated
                                df_hx.drop(df_hx.tail(1).index, inplace=True)

                            else:
                                df_hx.drop(columns=['Hot_Split', 'Cold_Split'], inplace=True)
                                all_combinations.append(deepcopy([df_streams_in, df_streams_out, df_hx]))


                               # for i in all_combinations:
                                #    print(i[2])


    return all_combinations



