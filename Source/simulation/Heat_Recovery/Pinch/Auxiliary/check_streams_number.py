
import numpy as np
from copy import deepcopy
import pandas as pd


def check_streams_number(df_streams_in, df_streams_out, above_pinch, delta_T_min, reach_pinch,check_time):
    """Check stream number rule

    This function aims to check one of the pinch analysis rule, which is that the number of streams_in <= streams_out.
    If this does not occur, multiple combinations and stream splits will be made to ensure that the number of
    streams_in and streams_out is equal.

    It was implemented the parameter reach_pinch, that is used at a first instance as reach_pinch=True to ensure that
    when all_first_match_pinch_combinations runs, all streams_in can be matched. At a second instance with
    reach_pinch=False, after all the first matches have been done.

    The function check_streams_number acts as main which runs split_streams as many time as the existent surplus number
    of streams in.

    Parameters
    ----------
    df_streams_in : df
        DF with streams going into the pinch

    df_streams_out : df
        DF with streams going out of the pinch

    above_pinch : boolean
        If above (TRUE) or below (FALSE) pinch analysis

    delta_T_min : float
        Minimum temperature difference [ºC]

    reach_pinch : boolean
        Whether streams reaches pinch temperature

    check_time : float
        Multiplier. To identify in which routine there is a stream split

    Returns
    -------
    all_combinations : list
        All combinations with [df_streams_in, df_streams_out] updated

    """
    ############################################################################################
    # Get info

    df_streams_in_copy = df_streams_in.copy()
    df_streams_out_copy = df_streams_out.copy()
    original_df_streams_in = deepcopy(df_streams_in)
    original_df_streams_out = deepcopy(df_streams_out)

    # create temporary key
    df_streams_in_copy['Split_Check'] = df_streams_in_copy['Split'].copy()
    df_streams_out_copy['Split_Check'] = df_streams_out_copy['Split'].copy()

    # get streams match info
    df_streams_in_copy_match_info = deepcopy(df_streams_in_copy['Match'])
    df_streams_out_copy_match_info = deepcopy(df_streams_out_copy['Match'])

    if reach_pinch == True:
        # change streams_in match meaning - check if complete match done - sometimes values are different by millesime
        df_streams_in_copy['Match'] = df_streams_in_copy.apply(
            lambda x: x['Match'] == True if x['Supply_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,
            axis=1)
        df_streams_out_copy['Match'] = df_streams_out_copy.apply(
            lambda x: x['Match'] == True if x['Target_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,
            axis=1)

    else:
        # change streams_in match meaning - check if complete match done - sometimes values are different by millesime
        df_streams_in_copy['Match'] = df_streams_in_copy.apply(
            lambda x: x['Match'] == True if x['Supply_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,
            axis=1)
        df_streams_out_copy['Match'] = df_streams_out_copy.apply(
            lambda x: x['Match'] == True if x['Target_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,
            axis=1)

    ############################################################################################
    # Get combinations

    # check if streams split is needed
    number_streams_out = df_streams_out_copy[
        df_streams_out_copy['Target_Temperature'] != round(df_streams_out_copy['Closest_Pinch_Temperature'], 1)].shape[0]
    number_streams_in = df_streams_in_copy[
        df_streams_in_copy['Supply_Temperature'] != round(df_streams_in_copy['Closest_Pinch_Temperature'], 1)].shape[0]

    all_combinations = [[df_streams_in_copy, df_streams_out_copy]]

    if number_streams_out < number_streams_in:
        if reach_pinch == True:
            surplus_streams_in = df_streams_in_copy[(df_streams_in_copy['Reach_Pinch'] == True) & (df_streams_in_copy['Match'] == False)].shape[0] - df_streams_out_copy[(df_streams_out_copy['Reach_Pinch'] == True) & (df_streams_out_copy['Match'] == False)].shape[0]
        else:
            surplus_streams_in = number_streams_in - number_streams_out

        # create all possibilities of stream splitting with a recursive function
        cycles = [0] * surplus_streams_in
        for cycle in cycles:
            all_combinations = split_streams(all_combinations, above_pinch, delta_T_min,check_time)

        # data treatment
        for dfs in all_combinations:
            df_streams_in_copy, df_streams_out_copy = dfs
            df_streams_out_copy['Match'] = df_streams_out_copy_match_info
            df_streams_out_copy.fillna(False, inplace=True)
            df_streams_in_copy['Match'] = df_streams_in_copy_match_info
            df_streams_in_copy.fillna(False, inplace=True)

    # delete temporary columns
    for combination in all_combinations:
        combination[0].drop(columns=['Split_Check'], inplace=True)
        combination[1].drop(columns=['Split_Check'], inplace=True)

    ############################################################################################
    # OUTPUT
    # eliminate repeated combinations
    if len(all_combinations) > 1:
        keep = [all_combinations[0]]
        for dfs_combination in all_combinations:
            append = True

            # get df streams out to compare with remaining
            dfs_combination_streams_out = dfs_combination[1].copy()
            dfs_combination_streams_out = dfs_combination_streams_out.sort_values('mcp')
            dfs_combination_streams_out.index = np.arange(1, len(dfs_combination_streams_out) + 1)

            # get df streams out to compare
            for dfs_keep in keep:
                dfs_keep_streams_out = dfs_keep[1].copy()
                dfs_keep_streams_out = dfs_keep_streams_out.sort_values('mcp')
                dfs_keep_streams_out.index = np.arange(1, len(dfs_keep_streams_out) + 1)

                if dfs_combination_streams_out['mcp'].equals(dfs_keep_streams_out['mcp']) != True and append == True:
                    append = True
                else:
                    append = False

            if append == True:
                keep.append(dfs_combination)

        all_combinations = keep
        all_combinations.append([original_df_streams_in, original_df_streams_out])


    elif len(all_combinations) == 1:
        for combination in all_combinations:
            df_streams_in, df_streams_out = combination
            df_streams_out['Match'] = df_streams_out_copy_match_info
            df_streams_in['Match'] = df_streams_in_copy_match_info

    else:
        all_combinations = [[original_df_streams_in, original_df_streams_out]]

    return all_combinations


def split_streams(combinations, above_pinch, delta_T_min, check_time):

    # init arrays
    combinations_updated = []

    # get combinations
    for combination in combinations:
        pairs = []
        df_streams_in, df_streams_out = combination

        # get first pair combinations between the streams to increase pinch analysis variability
        for index_stream_out in df_streams_out.index.values:
            for index_stream_in in df_streams_in.index.values:
                # get streams
                stream_out = df_streams_out.loc[index_stream_out]
                stream_in = df_streams_in.loc[index_stream_in]

                # only streams not yet split
                if stream_out['Split_Check'] == False and stream_in['Split_Check'] == False:

                    # only streams not yet matched
                    if stream_out['Match'] == False and stream_in['Match'] == False:

                        # only relevant to look for streams_out with larger mcp than streams_in
                        if stream_out['mcp'] > stream_in['mcp']:

                            # only relevant to look for streams_out whose temperature can meet streams_in temperature range
                            if (stream_out['Closest_Pinch_Temperature'] + delta_T_min < stream_in[
                                'Supply_Temperature'] and above_pinch is True) or (
                                    stream_out['Closest_Pinch_Temperature'] - delta_T_min > stream_in[
                                'Supply_Temperature'] and above_pinch is False):

                                if (stream_out['Closest_Pinch_Temperature'] + delta_T_min <= stream_in[
                                    'Closest_Pinch_Temperature'] and above_pinch is True) or (
                                        stream_out['Closest_Pinch_Temperature'] - delta_T_min >= stream_in[
                                    'Closest_Pinch_Temperature'] and above_pinch is False):
                                    pairs += [[index_stream_out, index_stream_in]]

        # match between pairs
        if pairs != []:
            for pair in pairs:
                # get dfs
                df_streams_in_copy = df_streams_in.copy()
                df_streams_out_copy = df_streams_out.copy()

                # get streams
                index_stream_out, index_stream_in = pair
                stream_in = df_streams_in_copy.loc[index_stream_in]
                stream_out = df_streams_out_copy.loc[index_stream_out]

                ###################################################################################
                # perform streams_in split
                if above_pinch == True:
                    # get streams info
                    hx_cold_stream_T_cold = stream_out['Closest_Pinch_Temperature']
                    cold_stream_max_T_hot = stream_out['Target_Temperature']
                    hot_stream_max_T_hot = stream_in['Supply_Temperature']
                    hx_hot_stream_T_cold = stream_in['Closest_Pinch_Temperature']
                    hot_stream_mcp = stream_in['mcp']

                    # compute/check temperatures
                    if hot_stream_max_T_hot >= (cold_stream_max_T_hot + delta_T_min):
                        hx_cold_stream_T_hot = cold_stream_max_T_hot
                    else:
                        hx_cold_stream_T_hot = hot_stream_max_T_hot - delta_T_min

                    hx_hot_stream_T_hot = hot_stream_max_T_hot
                    hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

                    # create split stream
                    split_stream_mcp = hx_power / (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
                    new_row = stream_out.copy()  # split stream has same info as original

                    # if split stream larger than stream mcp, find new hx_power
                    if new_row['mcp'] - split_stream_mcp < 0:
                        hx_hot_stream_T_hot = cold_stream_max_T_hot + delta_T_min
                        hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
                        split_stream_mcp = hx_power / (hx_cold_stream_T_hot - hx_cold_stream_T_cold)

                else:
                    # get streams info
                    hx_hot_stream_T_hot = stream_out['Supply_Temperature']
                    hot_stream_min_T_cold = stream_out['Target_Temperature']
                    cold_stream_mcp = stream_in['mcp']
                    cold_stream_min_T_cold = stream_in['Supply_Temperature']
                    hx_cold_stream_T_hot = stream_in['Closest_Pinch_Temperature']

                    # compute/check temperatures
                    if cold_stream_min_T_cold <= (hot_stream_min_T_cold - delta_T_min):
                        hx_hot_stream_T_cold = hot_stream_min_T_cold
                    else:
                        hx_hot_stream_T_cold = cold_stream_min_T_cold + delta_T_min

                    hx_cold_stream_T_cold = cold_stream_min_T_cold
                    hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)

                    # create split stream
                    split_stream_mcp = hx_power / (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
                    new_row = stream_out.copy()  # split stream has same info as original

                    # if split stream larger than stream mcp, find new hx_power
                    if new_row['mcp'] - split_stream_mcp < 0:
                        hx_cold_stream_T_cold = hot_stream_min_T_cold - delta_T_min
                        hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
                        split_stream_mcp = hx_power / (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

                # new row data
                new_row['mcp'] -= split_stream_mcp  # correct split mcp
                new_row['mcp'] = round(new_row['mcp'] + .0, 5)
                new_row.name = int(index_stream_out) * 10210 * check_time  # new ID
                new_row['Split_Check'] = False

                # add split stream to df
                df_streams_out_copy = pd.concat([df_streams_out_copy, pd.DataFrame([new_row])])


                # update dfs
                df_streams_out_copy.loc[index_stream_out, ['Split_Check']] = True
                df_streams_out_copy.loc[index_stream_out, ['Match']] = True
                df_streams_out_copy.loc[index_stream_out, ['mcp']] = round(split_stream_mcp + .0, 5)
                df_streams_in_copy.loc[index_stream_in, ['Match']] = True

                # safety check
                if new_row['mcp'] > 0:
                    combinations_updated.append([df_streams_in_copy, df_streams_out_copy])

        else:
            combinations_updated.append([df_streams_in, df_streams_out])


    return combinations_updated




