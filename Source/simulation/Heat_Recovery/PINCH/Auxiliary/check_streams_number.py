
"""
@author: jmcunha/alisboa

Info: Check if Streams In < Streams Out at pinch point. If not, split largest Stream Out to match largest mcp Stream In.

"""

from module.Source.simulation.Heat_Recovery.PINCH.Auxiliary.make_pairs import make_pairs

def check_streams_number(df_cold_streams,df_hot_streams,above_pinch,delta_T_min):


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

    # initial combination
    combinations = [[df_streams_out, df_streams_in]]

    # check if streams split is needed
    if df_streams_out.shape[0] < df_streams_in.shape[0]:

        surplus_streams_in = df_streams_in.shape[0] - df_streams_out.shape[0]

        # create all possibilities of stream splitting
        for cycle in range(surplus_streams_in - 1):
            combinations = make_pairs(combinations, above_pinch,delta_T_min)

    # delete temporary columns
    for combo in combinations:
        combo[0].drop(columns=['Split_Check'], inplace=True)
        combo[1].drop(columns=['Split_Check'], inplace=True)

    # OUTPUT
    if above_pinch == True:
        all_possibilities = combinations
    else:
        all_possibilities = [[combo[1], combo[0]] for combo in combinations]


    return all_possibilities





