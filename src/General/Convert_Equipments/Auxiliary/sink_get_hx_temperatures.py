def sink_get_hx_temperatures(grid_supply_temperature, grid_return_temperature, stream_supply_temperature, stream_target_temperature, hx_delta_T):
    """Compute for the hx between a grid and sink, its temperatures, according to the sink's streams temperature needs
      and the grid temperatures

    Parameters
    ----------
    grid_supply_temperature : float
        Grid supply temperature [ºC]

    grid_return_temperature : float
        Grid return temperature [ºC]

    stream_supply_temperature : float
        Stream supply temperature [ºC]

    stream_target_temperature : float
        Stream target temperature [ºC]

    hx_delta_T : float
        Heat exchanger minimum temperature difference [ºC]

    Returns
    -------
    hx_grid_supply_temperature : float
        Heat exchanger grid supply [ºC]

    hx_grid_target_temperature : float
        Heat exchanger grid target [ºC]

    hx_sink_supply_temperature : float
        Heat exchanger stream supply [ºC]

    hx_sink_target_temperature : float
        Heat exchanger stream target [ºC]

    """

    hx_grid_supply_temperature = grid_supply_temperature

    if grid_supply_temperature > stream_supply_temperature:
        if grid_supply_temperature > stream_target_temperature + hx_delta_T and grid_return_temperature > stream_supply_temperature + hx_delta_T:
            hx_grid_target_temperature = grid_return_temperature
            hx_sink_supply_temperature = stream_supply_temperature
            hx_sink_target_temperature = stream_target_temperature

        elif grid_supply_temperature > stream_target_temperature + hx_delta_T:
            hx_grid_target_temperature = stream_supply_temperature + hx_delta_T
            hx_sink_supply_temperature = stream_supply_temperature
            hx_sink_target_temperature = stream_target_temperature

        elif grid_supply_temperature < stream_target_temperature and grid_return_temperature > stream_supply_temperature + hx_delta_T:
            hx_grid_target_temperature = grid_return_temperature
            hx_sink_supply_temperature = stream_supply_temperature
            hx_sink_target_temperature = grid_supply_temperature - hx_delta_T

        else:
            hx_grid_target_temperature = stream_supply_temperature + hx_delta_T
            hx_sink_supply_temperature = stream_supply_temperature
            hx_sink_target_temperature = grid_supply_temperature - hx_delta_T

    else:
        hx_grid_supply_temperature = 1  # just to run
        hx_grid_target_temperature = 1
        hx_sink_supply_temperature = 1
        hx_sink_target_temperature = 1

    return hx_grid_supply_temperature, hx_grid_target_temperature, hx_sink_supply_temperature, hx_sink_target_temperature
