def above_pinch_stream_info(hot_stream, cold_stream):
    """Get streams above pinch info

    Parameters
    ----------
    hot_stream : dict
        Hot stream data, with the following keys:

            Closest_Pinch_Temperature : float
                [ºC]

            Supply_Temperature : float
                [ºC]

            Target_Temperature : float
                [ºC]

            mcp : float
                [kW/K]

            Fluid : str
                Fluid name

            Original_Stream : int
                Stream ID

    cold_stream : dict
        Cold stream data. Similar keys to "hot_stream"

    Returns
    -------
    hot_stream_T_cold : float
        [ºC]

    hot_stream_max_T_hot : float
        [ºC]

    hot_stream_mcp : float
        [kW/K]

    hot_stream_fluid : str

    cold_stream_T_cold : float
        [ºC]

    cold_stream_max_T_hot : float
        [ºC]

    cold_stream_mcp : float
        [kW/K]

    cold_stream_fluid : str

    original_hot_stream_index : int

    original_cold_stream_index : int

    """
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
