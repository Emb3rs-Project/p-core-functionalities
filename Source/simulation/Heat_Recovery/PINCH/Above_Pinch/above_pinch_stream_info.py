


def above_pinch_stream_info(hot_stream,cold_stream):

    hot_stream_T_cold = hot_stream['Closest_Pinch_Temperature']
    hot_stream_max_T_hot = hot_stream['Supply_Temperature']
    hot_stream_mcp = hot_stream['mcp']
    hot_stream_fluid = hot_stream['Fluid']
    cold_stream_T_cold = cold_stream['Closest_Pinch_Temperature']
    cold_stream_max_T_hot = cold_stream['Target_Temperature']
    cold_stream_mcp = cold_stream['mcp']
    cold_stream_fluid = cold_stream['Fluid']
    original_hot_stream_index = hot_stream['Original_Stream']
    original_cold_stream_index = cold_stream['Original_Stream']



    return  hot_stream_T_cold,hot_stream_max_T_hot,hot_stream_mcp,hot_stream_fluid,cold_stream_T_cold,cold_stream_max_T_hot,cold_stream_mcp,cold_stream_fluid,  original_hot_stream_index,original_cold_stream_index


