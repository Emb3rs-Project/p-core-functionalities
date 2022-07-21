
from ..Above_Pinch.above_pinch_hx_temperatures import above_pinch_hx_temperatures
from ..HX.design_hx import design_hx
from ..Above_Pinch.above_pinch_stream_info import above_pinch_stream_info
from ..Below_Pinch.below_pinch_stream_info import below_pinch_stream_info
from ..Below_Pinch.below_pinch_hx_temperatures import below_pinch_hx_temperatures
import pandas as pd
from copy import deepcopy
import numpy as np


def first_match_reach_pinch(kb, df_streams_in, df_streams_out, df_hx, hx_delta_T, above_pinch):
    """Match streams which reach pinch temperature

    The pinch design is always made from the pinch temperature to outwards. Thus, it is important to guarantee that all
    streams reaching pinch are well matched and that none is left.

    This script works similarly ot decision tree, where the function all_first_match_pinch_combinations acts as main
    which runs the recursive function make_combinations. This recursive function will make all possible match
    combinations of streams that reach pinch until all streams_in have been matched. This recursive function,
    maximizes pinch design variability by making all possible combinations between streams_in and streams_out, which
    may incur in new stream splits, and affect the following match. Even though it can be time consuming when a large
    number of streams is given, it has an added benefit of proposing more pinch designs.

    In brief when running make_combinations (which acts similarly to a decision tree), step by step:
      1) ** new state **
      2) get available streams_in and streams_out
      3) for cycle - fetch one stream_in
          4) for cycle - fetch one stream_out
              5) match and design hx (stream split may occur, adding new stream to respective df_streams_in or df_streams_out)
              6) update df_streams_in or df_streams_out

               if df_streams in not yet empty (meaning there are still streams_in reaching pinch):
                   7) call make_combinations and provide df_streams_in and df_streams_out updated - go to step 1
               else:
                   8) append design solution

    '9') when both for cycles reach the end, return to previous state (step 7 and jump to  step 4 or step 3)

    ** new state used here as the state of which the decision tree is **

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

    hx_delta_T :float
        Minimum HX temperature difference [ºC]

    above_pinch : boolean

    Returns
    -------
    all_combinations : list
        All combinations with [df_streams_in, df_streams_out,df_hx] updated

    """

    original_combination = deepcopy([df_streams_in, df_streams_out, df_hx])

    # Init arrays
    all_combinations = []

    # get all combinations with recursive function
    combination = deepcopy([df_streams_in, df_streams_out, df_hx])
    all_combinations = make_combinations(kb, combination, all_combinations, hx_delta_T, above_pinch)

    # eliminate repeated df_streams
    if len(all_combinations) > 1:
        keep_combinations = [all_combinations[0]]

        for combination in all_combinations:
            append = True
            combination_copy = combination[2].copy()
            combination_copy = combination_copy.sort_values('HX_Turnkey_Cost')
            combination_copy.index = np.arange(1, len(combination_copy) + 1)

            for keep_combination in keep_combinations:
                keep_combination_copy = keep_combination[2].copy()
                keep_combination_copy = keep_combination_copy.sort_values('HX_Turnkey_Cost')
                keep_combination_copy.index = np.arange(1, len(keep_combination_copy) + 1)

                if combination_copy[['HX_Power', 'HX_Turnkey_Cost']].equals(
                        keep_combination_copy[['HX_Power', 'HX_Turnkey_Cost']]) != True and append == True:
                    append = True
                else:
                    append = False

            if append == True:
                keep_combinations.append(combination)

        all_combinations = keep_combinations
        all_combinations.append(original_combination)

    elif len(all_combinations) == 0:
        all_combinations = [combination]

    return all_combinations


def make_combinations(kb, combination, all_combinations, hx_delta_T, above_pinch):

    # get streams and hx dfs
    combination_copy = deepcopy(combination)
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

        # create backup
        df_streams_in_backup = deepcopy(df_streams_in)
        df_streams_out.loc[stream_out_index, 'Match'] = False

        for stream_in_index in df_streams_in_for_index.index.values:

            # when recursive function goes step back, some values must be restored
            if save_index_out != -200:
                # restore stream out
                df_streams_out.loc[save_index_out] = deepcopy((combination_copy[1].loc[save_index_out]).copy())
                df_streams_out.loc[save_index_out, 'Match'] = False

            if save_index_in != -100:
                # restore dfs - needed because when splits are done, the original and the split need to be removed
                df_streams_in = df_streams_in_backup.copy()

            # restore initial Match value
            df_streams_out.loc[stream_out_index, 'Match'] = False
            df_streams_in.loc[stream_in_index, 'Match'] = False

            # get streams
            stream_out = df_streams_out.loc[stream_out_index]
            stream_in = df_streams_in.loc[stream_in_index]

            # analyze look for df_streams_out with smaller mcp than df_streams_in if number_stream_outs = number_stream_in
            # and for all streams_out with larger/equal mcp when number_stream_out >= number_stream_in
            if (stream_out['mcp'] <= stream_in['mcp'] and
                df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0] >
                df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0]) \
                    or (stream_out['mcp'] >= stream_in['mcp'] and
                        df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0] >=
                        df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0]):

                # only relevant to look for stream_out whose temperature can meet stream_in temperature range
                if (stream_out['Closest_Pinch_Temperature'] + hx_delta_T <
                    stream_in['Supply_Temperature'] and above_pinch == True) or (
                        stream_out['Closest_Pinch_Temperature'] - hx_delta_T >
                        stream_in['Supply_Temperature'] and above_pinch is False):

                    # only looking to streams which reach pinch
                    if stream_out['Reach_Pinch'] == True and stream_in['Reach_Pinch'] == True:

                        # only looking to streams which were not matched yet
                        if stream_in['Match'] == False and stream_out['Match'] == False:

                            # get streams info
                            if above_pinch == True:
                                stream_in_T_cold, stream_in_max_T_hot, stream_in_mcp, stream_in_fluid, stream_out_T_cold, \
                                stream_out_max_T_hot, stream_out_mcp, stream_out_fluid, original_stream_in_index, original_stream_out_index \
                                    = above_pinch_stream_info(stream_in,
                                                              stream_out)
                            else:
                                stream_out_min_T_cold, stream_out_T_hot, stream_out_mcp, stream_out_fluid, \
                                stream_in_min_T_cold, stream_in_T_hot, stream_in_mcp, stream_in_fluid, original_stream_out_index, \
                                original_stream_in_index = below_pinch_stream_info(stream_out,
                                                                                   stream_in)

                            # NO SPLIT
                            if stream_in_mcp <= stream_out_mcp:

                                # compute HX temperatures
                                if above_pinch == True:
                                    hx_power, hx_stream_in_T_cold, hx_stream_in_T_hot, hx_stream_out_T_cold, \
                                    hx_stream_out_T_hot = above_pinch_hx_temperatures(stream_in_T_cold,
                                                                                      stream_in_max_T_hot,
                                                                                      stream_in_mcp,
                                                                                      stream_out_T_cold,
                                                                                      stream_out_max_T_hot,
                                                                                      stream_out_mcp)
                                else:
                                    hx_power, hx_stream_out_T_cold, hx_stream_out_T_hot, hx_stream_in_T_cold, \
                                    hx_stream_in_T_hot = below_pinch_hx_temperatures(stream_out_T_hot,
                                                                                     stream_out_min_T_cold,
                                                                                     stream_out_mcp,
                                                                                     stream_in_T_hot,
                                                                                     stream_in_min_T_cold,
                                                                                     stream_in_mcp)

                            # SPLIT
                            else:
                                if above_pinch == True:
                                    hx_stream_out_T_cold = stream_out_T_cold

                                    # compute HX temperatures
                                    if stream_in_max_T_hot >= (stream_out_max_T_hot + hx_delta_T):
                                        hx_stream_out_T_hot = stream_out_max_T_hot
                                    else:
                                        hx_stream_out_T_hot = stream_in_max_T_hot - hx_delta_T

                                    hx_power = stream_out_mcp * (hx_stream_out_T_hot - hx_stream_out_T_cold)
                                    hx_stream_in_T_hot = stream_in_max_T_hot
                                    hx_stream_in_T_cold = stream_in_T_cold

                                    # create split stream
                                    split_stream_in_mcp = hx_power / (hx_stream_in_T_hot - hx_stream_in_T_cold)
                                    stream_in_mcp = split_stream_in_mcp  # update hot stream mcp
                                    new_row = deepcopy(stream_in.copy())  # split stream has same info as original
                                    new_row['mcp'] -= split_stream_in_mcp  # correct split mcp
                                    new_row.name = str(int(stream_in_index) * 100)  # new ID

                                    # add split stream to df
                                    df_streams_in = pd.concat([df_streams_in, pd.DataFrame([new_row])])


                                    hx_power, hx_stream_in_T_cold, hx_stream_in_T_hot, hx_stream_out_T_cold, hx_stream_out_T_hot\
                                        = above_pinch_hx_temperatures(stream_in_T_cold,
                                                                      stream_in_max_T_hot,
                                                                      stream_in_mcp,
                                                                      stream_out_T_cold,
                                                                      stream_out_max_T_hot,
                                                                      stream_out_mcp)

                                else:
                                    # compute/check temperatures
                                    if stream_in_min_T_cold <= (stream_out_min_T_cold - hx_delta_T):
                                        stream_out_T_cold = stream_out_min_T_cold
                                    else:
                                        stream_out_T_cold = stream_in_min_T_cold + hx_delta_T

                                    hx_power = stream_out_mcp * (stream_out_T_hot - stream_out_T_cold)
                                    hx_stream_in_T_cold = stream_in_min_T_cold

                                    # create split stream
                                    split_stream_in_mcp = hx_power / (stream_in_T_hot - hx_stream_in_T_cold)
                                    stream_in_mcp = split_stream_in_mcp  # update cold stream mcp
                                    new_row = deepcopy(stream_in.copy())  # split stream has same info as original
                                    new_row['mcp'] -= split_stream_in_mcp  # correct split mcp
                                    new_row.name = str(int(stream_in_index) * 100)  # new ID

                                    # add split stream to df
                                    df_streams_in = pd.concat([df_streams_in, pd.DataFrame([new_row])])

                                    hx_power, hx_stream_out_T_cold, hx_stream_out_T_hot, hx_stream_in_T_cold, hx_stream_in_T_hot\
                                        = below_pinch_hx_temperatures(stream_out_T_hot,
                                                                      stream_out_min_T_cold,
                                                                      stream_out_mcp,
                                                                      stream_in_T_hot,
                                                                      stream_in_min_T_cold,
                                                                      stream_in_mcp)

                                # update df_streams_in
                                df_streams_in.loc[stream_in_index, ['mcp']] = split_stream_in_mcp
                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_hot
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_hot
                                df_streams_in.loc[stream_in_index, ['Split']] = True

                            # save index in case the recursive iteration goes a step back
                            save_index_in = deepcopy(stream_in_index)
                            save_index_out = deepcopy(stream_out_index)

                            # update dfs
                            df_streams_out.loc[stream_out_index, ['Match']] = True
                            df_streams_in.loc[stream_in_index, ['Match']] = True

                            if above_pinch == True:
                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_hot
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_hot

                                # design HX
                                new_hx_row = design_hx(kb,
                                                       stream_in_index,
                                                       stream_out_index,
                                                       hx_stream_in_T_hot,
                                                       hx_stream_in_T_cold,
                                                       stream_in_fluid,
                                                       hx_stream_out_T_hot,
                                                       hx_stream_out_T_cold,
                                                       stream_out_fluid,
                                                       hx_power,
                                                       original_stream_in_index,
                                                       original_stream_out_index)


                            else:
                                df_streams_out.loc[stream_out_index, ['Closest_Pinch_Temperature']] = hx_stream_out_T_cold
                                df_streams_in.loc[stream_in_index, ['Closest_Pinch_Temperature']] = hx_stream_in_T_cold

                                # design HX
                                new_hx_row = design_hx(kb, stream_out_index,
                                                       stream_in_index,
                                                       hx_stream_out_T_hot,
                                                       hx_stream_out_T_cold,
                                                       stream_out_fluid,
                                                       hx_stream_in_T_hot,
                                                       hx_stream_in_T_cold,
                                                       stream_in_fluid,
                                                       hx_power,
                                                       original_stream_out_index,
                                                       original_stream_in_index)

                            df_hx = pd.concat([df_hx,  pd.DataFrame([new_hx_row])], ignore_index=True)

                            combination = deepcopy([df_streams_in, df_streams_out, df_hx])

                            ############################################################################################
                            # New decision tree ramification or append final design

                            # continue iteration or reach end and save
                            if df_streams_in[
                                (df_streams_in['Match'] == False) & (df_streams_in['Reach_Pinch'] == True)].shape[0] > 0:

                                try:
                                    all_combinations = make_combinations(kb, deepcopy(combination.copy()),
                                                                         deepcopy(all_combinations),
                                                                         hx_delta_T,
                                                                         above_pinch)
                                except:
                                    pass

                                # when iteration goes a step back, last HX designed must be eliminated
                                df_hx.drop(df_hx.tail(1).index, inplace=True)

                            else:
                                df_hx.drop(columns=['Hot_Split', 'Cold_Split'], inplace=True)
                                all_combinations.append(deepcopy([df_streams_in, df_streams_out, df_hx]))


    return all_combinations



