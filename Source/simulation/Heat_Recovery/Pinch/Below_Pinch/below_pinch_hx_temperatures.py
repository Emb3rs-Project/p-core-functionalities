""""
alisboa/jmcunha


##############################
INFO: Design HX power and temperatures for stream matches below pinch point. Design for maximum power exchange while
      checking temperatures feasibility on both streams.


##############################
INPUT:
        # hot_stream_T_hot  [ºC]
        # hot_stream_min_T_cold  [ºC]
        # hot_stream_mcp  [kW/K]
        # cold_stream_T_hot  [ºC]
        # cold_stream_min_T_cold  [ºC]
        # cold_stream_mcp  [kW/K]


##############################
RETURN:
        # hx_power  [kW]
        # hx_hot_stream_T_cold  [ºC]
        # hx_hot_stream_T_hot  [ºC]
        # hx_cold_stream_T_cold  [ºC]
        # hx_cold_stream_T_hot  [ºC]

"""

def below_pinch_hx_temperatures(hot_stream_T_hot, hot_stream_min_T_cold, hot_stream_mcp, cold_stream_T_hot,
                                cold_stream_min_T_cold, cold_stream_mcp):


    # max power available
    hx_cold_stream_T_hot = cold_stream_T_hot
    hx_hot_stream_T_hot = hot_stream_T_hot
    hx_hot_stream_T_cold = hot_stream_min_T_cold
    hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)

    # compute/check/correct temperatures
    hx_cold_stream_T_cold = hx_cold_stream_T_hot - hx_power / cold_stream_mcp

    if hx_cold_stream_T_cold < cold_stream_min_T_cold:
        hx_cold_stream_T_cold = cold_stream_min_T_cold
        hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
        hx_hot_stream_T_cold = hx_hot_stream_T_hot - hx_power / hot_stream_mcp

    else:
        hx_hot_stream_T_cold = hot_stream_min_T_cold


    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot

