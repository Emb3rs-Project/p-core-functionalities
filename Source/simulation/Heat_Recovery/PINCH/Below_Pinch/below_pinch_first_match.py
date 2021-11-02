from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_hx_temperatures import below_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.PINCH.HX.pinch_design_hx import pinch_design_hx
from ......Source.simulation.Heat_Recovery.PINCH.Below_Pinch.below_pinch_stream_info import below_pinch_stream_info


def below_pinch_first_match(df_hot_streams,df_cold_streams,df_hot_streams_dummy,df_cold_streams_dummy,df_hx,delta_T_min):


    while df_cold_streams_dummy.shape[0]>0:

        if df_hot_streams_dummy.empty == True:
            break

        # Cold Stream Max mcp
        cold_stream = df_cold_streams_dummy[df_cold_streams_dummy['mcp'] == max(df_cold_streams_dummy['mcp'].values)].iloc[0]
        cold_stream_index = cold_stream.name # get index

        # Hot Stream closest to Cold Stream mcp
        hot_stream_index = df_hot_streams_dummy.first_valid_index () # random initial index
        hot_stream = df_hot_streams_dummy.loc[hot_stream_index]
        dif = abs(cold_stream['mcp'] - df_hot_streams_dummy.loc[hot_stream_index]['mcp'])

        for index, row in df_hot_streams_dummy.iterrows():
            dif_new = abs(cold_stream['mcp'] - row['mcp'])
            if (dif_new < dif) or (dif_new == dif and row['mcp'] > hot_stream['mcp']): # prefer higher mcp
                dif = dif_new
                hot_stream_index = index
                hot_stream = df_hot_streams_dummy.loc[hot_stream_index]

        # Streams Info
        hot_stream_min_T_cold, hot_stream_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_min_T_cold, cold_stream_T_hot, cold_stream_mcp, cold_stream_fluid,original_hot_stream_index,original_cold_stream_index = below_pinch_stream_info(
            hot_stream, cold_stream)



        # NO SPLIT
        if cold_stream_mcp <= hot_stream_mcp:
            # Compute HX Temperatures
            hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = below_pinch_hx_temperatures(hot_stream_T_hot,hot_stream_min_T_cold,hot_stream_mcp,cold_stream_T_hot,cold_stream_min_T_cold,cold_stream_mcp)

        # SPLIT
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
            cold_stream_mcp = split_stream_mcp # update cold stream mcp

            new_row = cold_stream.copy() # split stream has same info
            new_row['mcp'] -= split_stream_mcp  # correct mcp
            new_row.name = str(int(cold_stream_index) * 100)  # new ID

            # Add Split Stream to DFs
            df_cold_streams_dummy = df_cold_streams_dummy.append(new_row)
            df_cold_streams = df_cold_streams.append(new_row)

            hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = below_pinch_hx_temperatures(hot_stream_T_hot,hot_stream_min_T_cold,hot_stream_mcp,cold_stream_T_hot,cold_stream_min_T_cold,cold_stream_mcp)


            # Update DFs
            df_cold_streams.loc[cold_stream_index, ['mcp']] = split_stream_mcp



        # Design HX
        new_hx_row = pinch_design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot, hx_hot_stream_T_cold,hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold,cold_stream_fluid, hx_power,original_hot_stream_index,original_cold_stream_index)

        df_hx = df_hx.append(new_hx_row, ignore_index=True)


        # 1st MATCH DONE - Drop Streams of DF PINCH
        df_cold_streams_dummy.drop(index=cold_stream_index, inplace=True)
        df_hot_streams_dummy.drop(index=hot_stream_index, inplace=True)

        # Update DF ORIGINAL
        df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_cold
        df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_cold
        df_cold_streams.loc[cold_stream_index, ['Match']] = True

        # Drop fulfilled streams DF ORIGINAL
        if df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']].values == df_hot_streams.loc[
            hot_stream_index, ['Target_Temperature']].values:
            df_hot_streams.drop(index=hot_stream_index, inplace=True)
        if df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']].values == df_cold_streams.loc[
            cold_stream_index, ['Supply_Temperature']].values:
            df_cold_streams.drop(index=cold_stream_index, inplace=True)



    return df_hot_streams,df_cold_streams,df_hx