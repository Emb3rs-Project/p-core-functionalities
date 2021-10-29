import copy

def match_remaining_streams_above_pinch_temperatures(
        hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, cold_stream_T_cold, cold_stream_max_T_hot, cold_stream_mcp):

    delta_T = 5
    find_T_vector = [5,1,0.1]
    cold_stream_T_hot_init = cold_stream_T_cold + 0.001 # initial guess
    hx_hot_stream_T_cold = hot_stream_T_cold
    hx_cold_stream_T_cold = copy.copy(cold_stream_T_cold)

    for step in find_T_vector:
        cold_stream_T_hot = copy.copy(cold_stream_T_hot_init)
        find_T = True

        while find_T == True:
            hx_cold_stream_T_hot = copy.copy(cold_stream_T_hot)
            hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
            hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp


            if (hx_hot_stream_T_hot > hot_stream_max_T_hot) or (hx_cold_stream_T_hot > cold_stream_max_T_hot) or (hx_cold_stream_T_hot + delta_T > hx_hot_stream_T_hot) :
                find_T = False

            else:
                cold_stream_T_hot_init = copy.copy(cold_stream_T_hot)
                cold_stream_T_hot = cold_stream_T_hot + step

    # Final Values
    hx_cold_stream_T_hot = cold_stream_T_hot_init
    hx_power = cold_stream_mcp * (hx_cold_stream_T_hot - hx_cold_stream_T_cold)
    hx_hot_stream_T_hot = hx_hot_stream_T_cold + hx_power / hot_stream_mcp


    return hx_power, hx_hot_stream_T_cold, hx_hot_stream_T_hot, hx_cold_stream_T_cold, hx_cold_stream_T_hot

