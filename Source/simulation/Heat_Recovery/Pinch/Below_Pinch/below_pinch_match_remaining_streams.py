from ......Source.simulation.Heat_Recovery.Pinch.Below_Pinch.below_pinch_hx_temperatures import below_pinch_hx_temperatures
from ......Source.simulation.Heat_Recovery.Pinch.HX.design_hx import design_hx
from ......Source.simulation.Heat_Recovery.Pinch.Below_Pinch.below_pinch_stream_info import below_pinch_stream_info
from ......Source.simulation.Heat_Recovery.Pinch.Below_Pinch.below_pinch_match_remaining_streams_temperatures import below_pinch_match_remaining_streams_temperatures


def below_pinch_match_remaining_streams(kb, hot_stream_index, hot_stream, cold_stream_index, cold_stream, df_cold_streams,
                                        df_hot_streams, hx_delta_T, restriction):

    """Design HX for streams given below pinch.

    Stream split not allowed for match_remaining_streams.
        1) When restriction=True, pinch analysis rule concerning concerning mcp_in<=mcp_out respected
        2) When restriction=False, pinch analysis rule concerning concerning mcp_in<=mcp_out not respected

    Parameters
    ----------
    kb : dict
        Knowledge Base data

    hot_stream_index :
        Hot stream ID

    hot_stream : dict
        Hot stream info

    cold_stream_index :
        Cold stream ID

    cold_stream : dict
        Cold stream info

    df_cold_streams : df
        Cold streams df

    df_hot_streams : df
        Hot streams df

    hx_delta_T : float
        Heat exchanger minimum temperature difference [ºC]

    restriction : boolean
        Consider restrictions (TRUE] or not (FALSE)

    Returns
    -------
    df_cold_streams : df
        Cold streams df updated

    df_hot_streams : df
        Hot streams df updated

    new_hx_row : df
        New HX designed for the streams provided

    """

    hx_cold_stream_T_cold = -200  # just to run
    hx_hot_stream_T_cold = -200  # just to run

    # streams info
    hot_stream_min_T_cold, hot_stream_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_min_T_cold, cold_stream_T_hot, \
    cold_stream_mcp, cold_stream_fluid, original_hot_stream_index, original_cold_stream_index \
        = below_pinch_stream_info(hot_stream, cold_stream)

    if hot_stream_T_hot > cold_stream_min_T_cold:
        if hot_stream_T_hot >= cold_stream_T_hot + hx_delta_T:

            if restriction == True:
                if cold_stream_mcp <= hot_stream_mcp:
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot \
                        = below_pinch_hx_temperatures(hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp,
                                                      cold_stream_T_hot,cold_stream_min_T_cold, cold_stream_mcp)

                    # design HX
                    new_hx_row = design_hx(kb, hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold,hot_stream_fluid, hx_cold_stream_T_hot,
                                                 hx_cold_stream_T_cold,cold_stream_fluid, hx_power,
                                                 original_hot_stream_index, original_cold_stream_index)
                else:
                    new_hx_row = []

            else:
                if hot_stream_T_hot + hx_delta_T > cold_stream_T_hot:  # must be larger
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot \
                        = below_pinch_match_remaining_streams_temperatures(hot_stream_T_hot, hot_stream_min_T_cold,
                                                                           hot_stream_mcp, cold_stream_T_hot,
                                                                           cold_stream_min_T_cold, cold_stream_mcp,hx_delta_T)

                    # Design HX
                    new_hx_row = design_hx(kb, hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold, hot_stream_fluid, hx_cold_stream_T_hot,
                                                 hx_cold_stream_T_cold, cold_stream_fluid, hx_power, original_hot_stream_index,
                                                 original_cold_stream_index)
                else:
                    new_hx_row = []
        else:
            new_hx_row = []
    else:
        new_hx_row = []

    # only necessary when original dfs are updated
    if hx_cold_stream_T_cold != -200 and hx_hot_stream_T_cold != -200:
        df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_cold
        df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_cold

    # drop rows from dfs
    if df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']].values == df_hot_streams.loc[
        hot_stream_index, ['Target_Temperature']].values:
        df_hot_streams.drop(index=hot_stream_index, inplace=True)

    if df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']].values == df_cold_streams.loc[
        cold_stream_index, ['Supply_Temperature']].values:
        df_cold_streams.drop(index=cold_stream_index, inplace=True)


    return df_cold_streams, df_hot_streams, new_hx_row