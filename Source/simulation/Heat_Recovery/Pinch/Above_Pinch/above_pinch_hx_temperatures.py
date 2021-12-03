""""
alisboa/jmcunha


##############################
INFO: Design HX power and temperatures for stream matches above pinch point. Design for maximum power exchange while
      checking temperatures feasibility on both streams.


##############################
INPUT:
        # hot_stream_T_cold  [ºC]
        # hot_stream_max_T_hot  [ºC]
        # hot_stream_mcp  [kW/K]
        # cold_stream_T_cold  [ºC]
        # cold_stream_max_T_hot  [ºC]
        # cold_stream_mcp  [kW/K]


##############################
RETURN:
        # hx_power  [kW]
        # hx_hot_stream_T_cold  [ºC]
        # hx_hot_stream_T_hot  [ºC]
        # hx_cold_stream_T_cold  [ºC]
        # hx_cold_stream_T_hot  [ºC]

"""


def above_pinch_hx_temperatures(hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold,
                                cold_stream_max_T_hot, cold_stream_mcp):

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