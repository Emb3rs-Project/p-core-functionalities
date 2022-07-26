def above_pinch_hx_temperatures(hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold,
                                cold_stream_max_T_hot, cold_stream_mcp):

    """Design HX power and temperatures for stream matches above pinch point.

    Design for maximum power exchange while checking temperatures feasibility on both streams.

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

    # max power available
    hx_hot_stream_T_cold = hot_stream_T_cold
    hx_cold_stream_T_cold = cold_stream_T_cold
    hx_power = cold_stream_mcp * (cold_stream_max_T_hot - cold_stream_T_cold)  # to obtain hx_hot_stream_T_hot first guess

    # compute/check/correct temperatures
    hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp

    if hx_hot_stream_T_hot >= hot_stream_max_T_hot:
        hx_hot_stream_T_hot = hot_stream_max_T_hot
        hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
        hx_cold_stream_T_hot = hx_cold_stream_T_cold + hx_power / cold_stream_mcp
    else:
        hx_cold_stream_T_hot = cold_stream_max_T_hot

    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot