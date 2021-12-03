""""
alisboa/jmcunha


##############################
INFO: After testing the code, two specific/special cases could occur that would not be solved due to the pinch analysis thought chain.
      This special cases were:
        1) when there is the same number of streams_in and streams_out (above or below pinch) and there is one stream_in with larger mcp than all streams_out
        2) when there is a stream_out with smaller mcp than all streams in



##############################
INPUT:



##############################
RETURN:

"""


def special_case(df_streams_in, df_streams_out, above_pinch,delta_T_min):

    # initial value
    split_needed = False
    special_case_1 = False
    special_case_2 = False
    pairs = []
    combinations_updated = []

    print('------------------------------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------------------------------')
    print('above_pinch',above_pinch)
    print(df_streams_in[['mcp']])
    print(df_streams_out[['mcp']])

    # Special Cases that happen when both dfs have same stream number
    if df_streams_in.shape[0] == df_streams_out.shape[0] or (df_streams_in[df_streams_in['Reach_Pinch'] == True].shape[0] == df_streams_out[df_streams_out['Reach_Pinch'] == True].shape[0]):

        # CASE 1 - check if there is a stream_in with larger mcp than all streams out
        index_streams_in_to_split = []
        for index,row in df_streams_in.iterrows():
            if (False in df_streams_out.apply(lambda x: True if x['mcp'] < row['mcp'] else False, axis=1).values) or ():
                pass
            else:
                split_needed = True
                special_case_1 = True
                index_streams_in_to_split.append(index)

        # CASE 2 - check if there is a stream_out with smaller mcp than all streams in:
        if split_needed == False:

            for index,row in df_streams_out.iterrows():
                if (False in df_streams_in.apply(lambda x: True if x['mcp'] > row['mcp'] else False, axis=1).values) :
                    pass
                else:
                    split_needed = True

            if split_needed == True:
                special_case_2 = True
                index_streams_in_to_split = df_streams_in.index.values


        if split_needed == True:

            ###########################################################################################################
            ################################################ CASE 1 ###################################################
            ###########################################################################################################

            if special_case_1 == True:
                print('special_case_1',special_case_1)

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
                        new_row.name = (int(hot_stream_index) * 100)  # new ID

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
                        new_row.name = (int(cold_stream_index) * 100)  # new ID
                        new_row['Split_Check'] = False

                        # Add Split Stream to DFs
                        df_streams_in = df_streams_in.append(new_row)

                        # Update DFs
                        df_streams_in.loc[index_stream_in]['Split_Check'] = True
                        df_streams_in.loc[cold_stream_index, ['mcp']] = split_stream_mcp

                    combinations_updated.append([df_streams_in_copy, df_streams_out_copy])

                all_combinations = combinations_updated

            ###########################################################################################################
            ################################################ CASE 2 ###################################################
            ###########################################################################################################

            elif special_case_2 == True:
                print('special_case_2',special_case_2)
                # get first pair combinations between the streams to increase pinch analysis variability
                for index_stream_out in df_streams_out.index.values:
                    for index_stream_in in index_streams_in_to_split:
                        # only relevant to look for streams_out whose temperature can meet streams_in temperature range
                        if (df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature'] + delta_T_min <
                            df_streams_in.loc[index_stream_in]['Supply_Temperature'] and above_pinch is True) or (
                                df_streams_out.loc[index_stream_out]['Closest_Pinch_Temperature'] - delta_T_min >
                                df_streams_in.loc[index_stream_in]['Supply_Temperature'] and above_pinch is False):
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

                        # stream_out larger mcp than stream_in
                        if df_streams_in_copy.loc[index_stream_in]['mcp'] < df_streams_out_copy.loc[index_stream_out]['mcp']:

                            # Compute/Check Temperatures
                            if hot_stream_max_T_hot >= (cold_stream_max_T_hot + delta_T_min):
                                hx_cold_stream_T_hot = cold_stream_max_T_hot
                            else:
                                hx_cold_stream_T_hot = hot_stream_max_T_hot - delta_T_min

                            # Split Stream Out
                            hx_power = hot_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
                            hx_hot_stream_T_hot = hot_stream_max_T_hot
                            hx_hot_stream_T_cold = hot_stream_T_cold

                            # Create Split Stream
                            split_cold_stream_mcp = hx_power / (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

                            new_row = cold_stream.copy()  # split stream has same info as original
                            new_row['mcp'] -= split_cold_stream_mcp  # correct split mcp
                            new_row.name = (int(cold_stream_index) * 700)  # new ID

                            new_row['Split_Check'] = True

                            # Add Split Stream to DFs
                            df_streams_out_copy = df_streams_out_copy.append(new_row)

                            # Update DFs
                            df_streams_out_copy.loc[cold_stream_index, ['Split_Check']] = True
                            df_streams_out_copy.loc[cold_stream_index, ['mcp']] = split_cold_stream_mcp

                        # stream_in larger mcp than stream_out
                        else:
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
                            new_row.name = (int(hot_stream_index) * 800)  # new ID

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
                        cold_stream_mcp = df_streams_in.loc[index_stream_in]['mcp']
                        cold_stream_T_hot = df_streams_in.loc[index_stream_in]['Closest_Pinch_Temperature']
                        cold_stream = df_streams_in.loc[index_stream_in]
                        cold_stream_index = index_stream_in
                        hot_stream_index = index_stream_out
                        hot_stream = df_streams_out.loc[index_stream_out]

                        # stream_out larger mcp than stream_in
                        if df_streams_in_copy.loc[index_stream_in]['mcp'] < df_streams_out_copy.loc[index_stream_out]['mcp']:

                            # Compute/Check Temperatures
                            if cold_stream_min_T_cold <= (hot_stream_min_T_cold - delta_T_min):
                                hot_stream_T_cold = hot_stream_min_T_cold
                            else:
                                hot_stream_T_cold = cold_stream_min_T_cold + delta_T_min

                            cold_stream_T_cold = cold_stream_min_T_cold
                            hx_power = cold_stream_mcp * (cold_stream_T_hot - cold_stream_T_cold)

                            # Create Split Stream
                            split_stream_mcp = hx_power / (hot_stream_T_hot - hot_stream_T_cold)

                            new_row = hot_stream.copy()  # split stream has same info
                            new_row['mcp'] -= split_stream_mcp  # correct mcp
                            new_row.name = (int(hot_stream_index) * 100)  # new ID
                            new_row['Split_Check'] = False

                            # Add Split Stream to DFs
                            df_streams_out_copy = df_streams_out_copy.append(new_row)

                            # Update DFs
                            df_streams_out_copy.loc[hot_stream_index]['Split_Check'] = True
                            df_streams_out_copy.loc[hot_stream_index, ['mcp']] = split_stream_mcp

                        else:

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
                            new_row.name = (int(cold_stream_index) * 100)  # new ID
                            new_row['Split_Check'] = False

                            # Add Split Stream to DFs
                            df_streams_in_copy = df_streams_in_copy.append(new_row)

                            # Update DFs
                            df_streams_in_copy.loc[index_stream_in]['Split_Check'] = True
                            df_streams_in_copy.loc[cold_stream_index, ['mcp']] = split_stream_mcp

                    combinations_updated.append([df_streams_in_copy, df_streams_out_copy])



                all_combinations = combinations_updated
                all_combinations.append([df_streams_in, df_streams_out])


        else:
            all_combinations = [[df_streams_in ,df_streams_out]]

    else:
        all_combinations = [[df_streams_in, df_streams_out]]

    return all_combinations