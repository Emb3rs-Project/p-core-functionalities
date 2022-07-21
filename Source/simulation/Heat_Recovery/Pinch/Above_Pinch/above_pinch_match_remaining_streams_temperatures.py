import copy


def above_pinch_match_remaining_streams_temperatures(
        hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot,
        cold_stream_mcp, hx_delta_T):

    """Design HX temperatures for streams above pinch.

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
    cold_stream_T_hot_init = cold_stream_T_cold + 0.001  # initial guess
    hx_hot_stream_T_cold = hot_stream_T_cold
    hx_cold_stream_T_cold = copy.copy(cold_stream_T_cold)

    # iterative process to find temperature
    for step in find_T_vector:
        cold_stream_T_hot = copy.copy(cold_stream_T_hot_init)
        find_T = True

        while find_T == True:
            hx_cold_stream_T_hot = copy.copy(cold_stream_T_hot)
            hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
            hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp

            if (hx_hot_stream_T_hot > hot_stream_max_T_hot) or (hx_cold_stream_T_hot > cold_stream_max_T_hot) or (
                    hx_cold_stream_T_hot + hx_delta_T > hx_hot_stream_T_hot):
                find_T = False

            else:
                cold_stream_T_hot_init = copy.copy(cold_stream_T_hot)
                cold_stream_T_hot = cold_stream_T_hot + step

    # final values
    hx_cold_stream_T_hot = cold_stream_T_hot_init
    hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
    hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp

    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot
