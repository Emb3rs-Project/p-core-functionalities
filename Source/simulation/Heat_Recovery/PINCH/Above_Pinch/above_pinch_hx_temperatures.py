""""
jmcunha/alisboa

Info: Compute HX temperatures Above Pinch Point Analysis.

"""

def above_pinch_hx_temperatures(hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot, cold_stream_mcp):


    # Max Power Available
    hx_hot_stream_T_cold = hot_stream_T_cold
    hx_cold_stream_T_cold = cold_stream_T_cold
    hx_power = cold_stream_mcp * (cold_stream_max_T_hot - cold_stream_T_cold)

    # Compute/Check/Correct Temperatures
    hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp

    if hx_hot_stream_T_hot > hot_stream_max_T_hot:
        hx_hot_stream_T_hot = hot_stream_max_T_hot
        hx_power = hot_stream_mcp * (hx_hot_stream_T_hot - hx_hot_stream_T_cold)
        hx_cold_stream_T_hot = hx_cold_stream_T_cold + hx_power / cold_stream_mcp
    else:
        hx_cold_stream_T_hot = cold_stream_max_T_hot

    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot