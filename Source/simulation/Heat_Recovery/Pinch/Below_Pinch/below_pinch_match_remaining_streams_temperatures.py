""""
alisboa/jmcunha


##############################
INFO: Design HX temperatures for streams below pinch.
      Iterative process to find temperatures.


##############################
INPUT:
        # hot_stream_T_hot
        # hot_stream_min_T_cold
        # hot_stream_mcp
        # cold_stream_T_hot
        # cold_stream_min_T_cold
        # cold_stream_mcp
        # hx_delta_T


##############################
RETURN:
        # hx_power
        # hx_hot_stream_T_cold
        # hx_hot_stream_T_hot
        # hx_cold_stream_T_cold
        # hx_cold_stream_T_hot

"""
import copy


def below_pinch_match_remaining_streams_temperatures(
        hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp, cold_stream_T_hot, cold_stream_min_T_cold,
        cold_stream_mcp, hx_delta_T):

    find_T_vector = [5, 1, 0.1]
    hot_stream_T_cold_init = hot_stream_T_hot - 0.001  # initial guess
    hx_hot_stream_T_hot = hot_stream_T_hot
    hx_cold_stream_T_hot = copy.copy(cold_stream_T_hot)

    # iterative process to find temperature
    for step in find_T_vector:
        hot_stream_T_cold = copy.copy(hot_stream_T_cold_init)
        find_T = True

        while find_T == True:
            hx_hot_stream_T_cold = copy.copy(hot_stream_T_cold)
            hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
            hx_cold_stream_T_cold = hx_cold_stream_T_hot - hx_power / cold_stream_mcp

            if (hx_hot_stream_T_cold < hot_stream_min_T_cold) or (hx_cold_stream_T_cold < cold_stream_min_T_cold) or (
                    hx_hot_stream_T_cold < hx_cold_stream_T_cold + hx_delta_T):
                find_T = False

            else:
                hot_stream_T_cold_init = copy.copy(hot_stream_T_cold)
                hot_stream_T_cold = hot_stream_T_cold - step

    # final values
    hx_hot_stream_T_cold = hot_stream_T_cold_init
    hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
    hx_cold_stream_T_cold = hx_cold_stream_T_hot - hx_power / cold_stream_mcp

    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot
