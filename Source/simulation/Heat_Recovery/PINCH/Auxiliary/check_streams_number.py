
"""
@author: jmcunha/alisboa

Info: Check if Streams In < Streams Out at pinch point. If not, split largest Stream Out to match largest mcp Stream In.

"""

from .make_pairs import make_pairs
import numpy as np
from copy import deepcopy

def check_streams_number(df_cold_streams,df_hot_streams,above_pinch,delta_T_min,reach_pinch):

    perform_special_case = False

    # check if above/below pinch
    if above_pinch == True:
        df_streams_in = df_hot_streams.copy()
        df_streams_out = df_cold_streams.copy()
    else:
        df_streams_in = df_cold_streams.copy()
        df_streams_out = df_hot_streams.copy()

    # create temporary key
    df_streams_in['Split_Check'] = False
    df_streams_out['Split_Check'] = False

    # get match info
    df_streams_in_match_info = deepcopy(df_streams_in['Match'])
    df_streams_out_match_info = deepcopy(df_streams_out['Match'])

    # initial combination
    combinations = [[df_streams_out, df_streams_in]]

    number_streams_out = df_streams_out[df_streams_out['Target_Temperature'] != round(df_streams_out['Closest_Pinch_Temperature'] , 1)].shape[0]
    number_streams_in = df_streams_in[df_streams_in['Supply_Temperature'] != round(df_streams_in['Closest_Pinch_Temperature'] , 1)].shape[0]

    # check if streams split is needed
    if number_streams_out < number_streams_in:

        if reach_pinch == True:
            surplus_streams_in = df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0] - df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0]
            cycles = [0] * surplus_streams_in
            # create all possibilities of stream splitting by doing a for loop wher output goes as input
            for cycle in cycles:
                combinations = make_pairs(combinations, above_pinch,delta_T_min,perform_special_case)
        else:
            surplus_streams_in = number_streams_in - number_streams_out
            cycles = [0] * surplus_streams_in
            # create all possibilities of stream splitting by doing a for loop wher output goes as input
            for cycle in cycles:
                combinations = make_pairs(combinations, above_pinch,delta_T_min,perform_special_case)



        for dfs in combinations:
            df_streams_out, df_streams_in = dfs
            df_streams_out['Match'] = df_streams_out_match_info
            df_streams_out.fillna(False, inplace=True)
            df_streams_in['Match'] = df_streams_in_match_info
            df_streams_in.fillna(False, inplace=True)


        # Last resource - if above does not work
        for dfs in combinations:
            df_hot,df_cold = dfs

            if df_hot.shape[0] >= df_cold.shape[0]:
                if df_hot['Reach_Pinch'].shape[0] >= df_cold['Reach_Pinch'].shape[0]:
                    pass
                else:
                    perform_special_case = True
            else:
                perform_special_case = True

        if perform_special_case == True:
            for cycle in cycles:
                combinations = make_pairs(combinations, above_pinch,delta_T_min,perform_special_case)

            for dfs in combinations:
                df_streams_out, df_streams_in = dfs
                df_streams_out['Match'] = df_streams_out_match_info
                df_streams_in['Match'] = df_streams_in_match_info





    # delete temporary columns
    for combo in combinations:
        combo[0].drop(columns=['Split_Check'], inplace=True)
        combo[1].drop(columns=['Split_Check'], inplace=True)

    # OUTPUT
    if above_pinch == True:
        all_possibilities = combinations
    else:
        all_possibilities = [[combo[1], combo[0]] for combo in combinations]


    if len(all_possibilities) > 1:
        keep = []
        keep.append(all_possibilities[0])
        for i in all_possibilities:
            append = True

            i_copy = i[0].copy()
            i_copy = i_copy.sort_values('mcp')

            i_copy.index = np.arange(1, len(i_copy) + 1)

            for j in keep:
                j_copy = j[0].copy()
                j_copy = j_copy.sort_values('mcp')
                j_copy.index = np.arange(1, len(j_copy) + 1)

                if i_copy['mcp'].equals(j_copy['mcp']) != True and append == True:
                    append = True
                else:
                    append = False


            if append == True:
                keep.append(i)

        all_possibilities = keep


    return all_possibilities





