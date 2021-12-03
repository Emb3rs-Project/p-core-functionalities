""""
alisboa/jmcunha


##############################
INFO: Get streams above pinch info


##############################
INPUT:
        # hot_stream
        # cold_stream

        Where in hot_stream/cold_stream, the following keys:
            # Closest_Pinch_Temperature
            # Supply_Temperature
            # Target_Temperature
            # mcp
            # Fluid
            # Original_Stream


##############################
RETURN:
        # hot_stream_T_cold  [ºC]
        # hot_stream_max_T_hot  [ºC]
        # hot_stream_mcp  [kW/K]
        # hot_stream_fluid  [fluid]
        # original_hot_stream_index  [ID]
        # cold_stream_T_cold  [ºC]
        # cold_stream_max_T_hot  [ºC]
        # cold_stream_mcp  [kW/K]
        # cold_stream_fluid  [fluid]
        # original_cold_stream_index  [ID]

"""

def above_pinch_stream_info(hot_stream, cold_stream):

    hot_stream_T_cold = hot_stream['Closest_Pinch_Temperature']
    hot_stream_max_T_hot = hot_stream['Supply_Temperature']
    hot_stream_mcp = hot_stream['mcp']
    hot_stream_fluid = hot_stream['Fluid']
    original_hot_stream_index = hot_stream['Original_Stream']

    cold_stream_T_cold = cold_stream['Closest_Pinch_Temperature']
    cold_stream_max_T_hot = cold_stream['Target_Temperature']
    cold_stream_mcp = cold_stream['mcp']
    cold_stream_fluid = cold_stream['Fluid']
    original_cold_stream_index = cold_stream['Original_Stream']

    return hot_stream_T_cold, hot_stream_max_T_hot, hot_stream_mcp, hot_stream_fluid, cold_stream_T_cold, cold_stream_max_T_hot, \
           cold_stream_mcp, cold_stream_fluid, original_hot_stream_index, original_cold_stream_index
