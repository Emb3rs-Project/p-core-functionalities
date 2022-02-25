""""
alisboa/jmcunha


##############################
INFO: Design HX for streams given above pinch. Stream split not allowed for match_remaining_streams.
        1) When restriction=True, pinch analysis rule concerning concerning mcp_in<=mcp_out respected
        2) When restriction=False, pinch analysis rule concerning concerning mcp_in<=mcp_out not respected


##############################
INPUT:
        # hot_stream_index
        # hot_stream
        # cold_stream_index
        # cold_stream
        # df_cold_streams
        # df_hot_streams
        # hx_delta_T
        # restriction  [True or False]


##############################
RETURN:
        # df_cold_streams - updated
        # df_hot_streams - updated
        # new_hx_row - design HX for the streams provided

"""


from ......Source.simulation.Heat_Recovery.Pinch.Above_Pinch.above_pinch_hx_temperatures import above_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.Pinch.HX.design_hx import design_hx
from ......Source.simulation.Heat_Recovery.Pinch.Above_Pinch.above_pinch_stream_info import above_pinch_stream_info
from module.Source.simulation.Heat_Recovery.Pinch.Above_Pinch.above_pinch_match_remaining_streams_temperatures import above_pinch_match_remaining_streams_temperatures


def above_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream, cold_stream_index, cold_stream, df_cold_streams,
                                        df_hot_streams, hx_delta_T, restriction):

    hx_hot_stream_T_hot = -200  # just to run
    hx_cold_stream_T_hot = -200  # just to run

    # streams info
    hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_T_cold, cold_stream_max_T_hot, \
    cold_stream_mcp, cold_stream_fluid, original_hot_stream_index, original_cold_stream_index \
        = above_pinch_stream_info(hot_stream, cold_stream)

    # check/match streams
    if hot_stream_max_T_hot > cold_stream_T_cold:
        if hot_stream_T_cold >= cold_stream_T_cold + hx_delta_T:

            if restriction == True:
                if hot_stream_mcp <= cold_stream_mcp:
                    # compute HX temperatures
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot \
                        = above_pinch_hx_temperatures(hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp,
                                                      cold_stream_T_cold, cold_stream_max_T_hot, cold_stream_mcp)
                    # design HX
                    new_hx_row = design_hx(kb, hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold, hot_stream_fluid, hx_cold_stream_T_hot,
                                                 hx_cold_stream_T_cold, cold_stream_fluid, hx_power,
                                                 original_hot_stream_index, original_cold_stream_index)
                else:
                    new_hx_row = []

            else:
                if hot_stream_T_cold > cold_stream_T_cold + hx_delta_T:
                    # compute HX temperatures
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot \
                        = above_pinch_match_remaining_streams_temperatures(hot_stream_T_cold, hot_stream_max_T_hot,
                                                                           hot_stream_mcp, cold_stream_T_cold,
                                                                           cold_stream_max_T_hot, cold_stream_mcp,hx_delta_T)

                    # design HX
                    new_hx_row = design_hx(kb, hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold, hot_stream_fluid, hx_cold_stream_T_hot,
                                                 hx_cold_stream_T_cold, cold_stream_fluid, hx_power,
                                                 original_hot_stream_index, original_cold_stream_index)
                else:
                    new_hx_row = []
        else:
            new_hx_row = []
    else:
        new_hx_row = []

    # only necessary when original dfs are updated
    if hx_hot_stream_T_hot != -200 and hx_cold_stream_T_hot != -200:
        df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_hot
        df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_hot

    # drop rows from dfs
    if df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']].values == df_hot_streams.loc[
        hot_stream_index, ['Supply_Temperature']].values:
        df_hot_streams.drop(index=hot_stream_index, inplace=True)

    if df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']].values == df_cold_streams.loc[
        cold_stream_index, ['Target_Temperature']].values:
        df_cold_streams.drop(index=cold_stream_index, inplace=True)


    return df_cold_streams, df_hot_streams, new_hx_row