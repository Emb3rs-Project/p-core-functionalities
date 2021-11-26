""""
alisboa/jmcunha

##############################
INFO: ACheck if Streams In < Streams Out at pinch point. If not, split largest Stream Out to match largest mcp Stream In.

##############################
INPUT:
        # df_streams_in
        # df_streams_out
        # above_pinch
        # delta_T_min
        # reach_pinch

##############################
RETURN:
        # [[df_streams_in, df_streams_out], ...

"""

import numpy as np
from copy import deepcopy

def testing_check_streams_number(df_streams_in, df_streams_out, above_pinch, delta_T_min, reach_pinch,check_time):

    ############################################################################################
    # Get info
    # copy dfs
    df_streams_in_copy = df_streams_in.copy()
    df_streams_out_copy = df_streams_out.copy()

    # create temporary key
    df_streams_in_copy['Split_Check'] = False
    df_streams_out_copy['Split_Check'] = False

    # get streams match info
    df_streams_in_copy_match_info = deepcopy(df_streams_in_copy['Match'])
    df_streams_out_copy_match_info = deepcopy(df_streams_out_copy['Match'])


    # change streams_in match meaning - check if complete match done - sometimes values are different by millesime
    df_streams_in_copy['Match'] = df_streams_in_copy.apply(lambda x: x['Match'] == True if x['Supply_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,axis=1)
    ########## NEW &%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    df_streams_out_copy['Match'] = df_streams_out_copy.apply(lambda x: x['Match'] == True if x['Target_Temperature'] == round(x['Closest_Pinch_Temperature']) else False,axis=1)

    ############################################################################################
    # Get combinations
    # check if streams split is needed


    combinations = [[df_streams_in_copy, df_streams_out_copy]]
    number_streams_out = df_streams_out_copy[df_streams_out_copy['Target_Temperature'] != round(df_streams_out_copy['Closest_Pinch_Temperature'], 1)].shape[0]
    number_streams_in = df_streams_in_copy[ df_streams_in_copy['Supply_Temperature'] != round(df_streams_in_copy['Closest_Pinch_Temperature'], 1)].shape[0]

    if number_streams_out < number_streams_in:
        if reach_pinch == True:
            surplus_streams_in = df_streams_in_copy[df_streams_in_copy['Reach_Pinch'] == True].shape[0] - df_streams_out_copy[df_streams_out_copy['Reach_Pinch'] == True].shape[0]
        else:
            surplus_streams_in = number_streams_in - number_streams_out

        # create all possibilities of stream splitting with a recursive function
        cycles = [0] * surplus_streams_in
        for cycle in cycles:
            combinations = make_pairs(combinations, above_pinch, delta_T_min,check_time)

        # data treatment
        for dfs in combinations:
            df_streams_in_copy, df_streams_out_copy = dfs
            df_streams_out_copy['Match'] = df_streams_out_copy_match_info
            df_streams_out_copy.fillna(False, inplace=True)
            df_streams_in_copy['Match'] = df_streams_in_copy_match_info
            df_streams_in_copy.fillna(False, inplace=True)

    # delete temporary columns
    for combination in combinations:
        combination[0].drop(columns=['Split_Check'], inplace=True)
        combination[1].drop(columns=['Split_Check'], inplace=True)

    ############################################################################################
    # OUTPUT
    # eliminate repeated combinations
    if len(combinations) > 1:
        keep = [combinations[0]]
        for dfs_combination in combinations:
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
        combinations = keep

    return combinations


def make_pairs(combinations, above_pinch,delta_T_min,check_time):

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
                            if (stream_out['Closest_Pinch_Temperature'] + delta_T_min < stream_in['Supply_Temperature'] and above_pinch is True) or (stream_out['Closest_Pinch_Temperature'] - delta_T_min > stream_in['Supply_Temperature'] and above_pinch is False):

                                if (stream_out['Closest_Pinch_Temperature'] + delta_T_min <= stream_in['Closest_Pinch_Temperature'] and above_pinch is True) or (stream_out['Closest_Pinch_Temperature'] - delta_T_min >= stream_in['Closest_Pinch_Temperature'] and above_pinch is False):
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
                new_row.name = int(index_stream_out) * 100 * check_time  # new ID
                new_row['Split_Check'] = False

                # add split stream to df
                df_streams_out_copy = df_streams_out_copy.append(new_row)

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




