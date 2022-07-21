
import copy


def below_pinch_match_remaining_streams_temperatures(hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp, cold_stream_T_hot,
                                                     cold_stream_min_T_cold, cold_stream_mcp, hx_delta_T):

    """Design HX temperatures for streams below pinch.

    Iterative process to find temperatures.

    Parameters
    ----------
    hot_stream_T_cold : float
        [ºC]

    hot_stream_max_T_hot : float
        [ºC]

    hot_stream_mcp : float
        [kW/K]

    cold_stream_T_cold : float
        [ºC]

    cold_stream_max_T_hot : float
        [ºC]

    cold_stream_mcp : float
        [kW/K]

    hx_delta_T : float
        [ºC]

    Returns
    -------
    hx_power : float
        [kW]

    hx_hot_stream_T_cold : float
        [ºC]

    hx_hot_stream_T_hot : float
        [ºC]

    hx_cold_stream_T_cold : float
        [ºC]

    hx_cold_stream_T_hot : float
        [ºC]

    """

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
