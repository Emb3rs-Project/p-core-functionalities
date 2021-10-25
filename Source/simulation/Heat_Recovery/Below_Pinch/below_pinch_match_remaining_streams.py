""""
jmcunha/alisboa

Info: Match remaining streams above pinch. When restriction=True, activated pinch analysis rules concerning mcp_in<mcp_out.
      No splits are allowed.

"""

from Source.simulation.Heat_Recovery.Below_Pinch.below_pinch_hx_temperatures import below_pinch_hx_temperatures
from Source.simulation.Heat_Recovery.HX.pinch_design_hx import pinch_design_hx
from Source.simulation.Heat_Recovery.Below_Pinch.below_pinch_stream_info import below_pinch_stream_info
from Source.simulation.Heat_Recovery.Auxiliary.match_remaining_streams_below_pinch_temperatures import match_remaining_streams_below_pinch_temperatures

def below_pinch_match_remaining_streams(hot_stream_index, hot_stream, cold_stream_index, cold_stream, df_cold_streams, df_hot_streams,delta_T_min, restriction):

    # Streams Info
    hot_stream_min_T_cold, hot_stream_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_min_T_cold, cold_stream_T_hot, cold_stream_mcp, cold_stream_fluid,original_hot_stream_index,original_cold_stream_index = below_pinch_stream_info(
        hot_stream, cold_stream)

    hx_cold_stream_T_cold = 0 # just to run
    hx_hot_stream_T_cold = 0 # just to run

    if hot_stream_T_hot > cold_stream_min_T_cold:
        if hot_stream_T_hot >= cold_stream_T_hot + delta_T_min:
            if restriction == True:
                if cold_stream_mcp <= hot_stream_mcp:
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = below_pinch_hx_temperatures(
                        hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp, cold_stream_T_hot,
                        cold_stream_min_T_cold, cold_stream_mcp)

                    # Design HX
                    new_hx_row = pinch_design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold,
                                                 hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold,
                                                 cold_stream_fluid, hx_power, original_hot_stream_index,original_cold_stream_index)
                else:
                    new_hx_row = []

            else:
                if hot_stream_T_hot + delta_T_min > cold_stream_T_hot: # must be larger
                    hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot = match_remaining_streams_below_pinch_temperatures(
                        hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp, cold_stream_T_hot, cold_stream_min_T_cold,
                        cold_stream_mcp)

                    # Design HX
                    new_hx_row = pinch_design_hx(hot_stream_index, cold_stream_index, hx_hot_stream_T_hot,
                                                 hx_hot_stream_T_cold,
                                                 hot_stream_fluid, hx_cold_stream_T_hot, hx_cold_stream_T_cold,
                                                 cold_stream_fluid, hx_power,original_hot_stream_index,original_cold_stream_index)
                else:
                    new_hx_row = []

        else:
            new_hx_row = []
    else:
        new_hx_row = []

    # UPDATE DF ORIGINAL
    df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']] = hx_cold_stream_T_cold
    df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']] = hx_hot_stream_T_cold

    # DROP DF ORIGINAL
    if df_hot_streams.loc[hot_stream_index, ['Closest_Pinch_Temperature']].values == df_hot_streams.loc[
        hot_stream_index, ['Target_Temperature']].values:
        df_hot_streams.drop(index=hot_stream_index, inplace=True)

    if df_cold_streams.loc[cold_stream_index, ['Closest_Pinch_Temperature']].values == df_cold_streams.loc[
        cold_stream_index, ['Supply_Temperature']].values:
        df_cold_streams.drop(index=cold_stream_index, inplace=True)


    return df_cold_streams, df_hot_streams, new_hx_row