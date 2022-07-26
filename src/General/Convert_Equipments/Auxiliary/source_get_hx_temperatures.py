def source_get_hx_temperatures(hx_grid_stream_target_temperature, hx_grid_stream_supply_temperature,source_stream_supply_temperature,
                               source_stream_target_temperature, hx_delta_T):

    """Compute temperatures for the HX between source and grid

    Parameters
    ----------
    hx_grid_stream_target_temperature : float
        Grid target temperature [ºC]

    hx_grid_stream_supply_temperature : float
        Grid supply temperature [ºC]

    source_stream_supply_temperature : float
        Stream supply temperature [ºC]

    source_stream_target_temperature : float
        Stream target temperature [ºC]

    hx_delta_T : float
        Heat exchanger minimum temperature difference [ºC]


    Returns
    -------
    hx_grid_stream_supply_temperature : float
        Heat exchanger grid supply [ºC]

    hx_grid_stream_target_temperature : float
        Heat exchanger grid target [ºC]

    hx_source_stream_supply_temperature : float
        Heat exchanger stream supply [ºC]

    hx_source_stream_target_temperature : float
        Heat exchanger stream target [ºC]


    """

    hx_source_stream_supply_temperature = source_stream_supply_temperature

    # if source stream target_temperature > hx_grid
    if source_stream_target_temperature > hx_grid_stream_supply_temperature + hx_delta_T:
        hx_source_stream_target_temperature = source_stream_target_temperature

    else:  # stream_target_temperature < grid_stream_supply_temperature + hx_delta_T:
        hx_source_stream_target_temperature = hx_grid_stream_supply_temperature + hx_delta_T

        if hx_source_stream_target_temperature < source_stream_target_temperature:
            hx_source_stream_target_temperature = source_stream_target_temperature


    return hx_grid_stream_supply_temperature, hx_grid_stream_target_temperature, hx_source_stream_supply_temperature, hx_source_stream_target_temperature
