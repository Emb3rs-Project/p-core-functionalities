"""
alisboa/jmcunha


##############################
INFO: compute for the hx between a grid and sink, its temperatures, according to the sink's streams temperature needs
      and the grid temperatures


##############################
INPUT:
        # grid_supply_temperature  [ºC]
        # grid_return_temperature  [ºC]
        # stream_supply_temperature  [ºC]
        # stream_target_temperature  [ºC]
        # hx_delta_T


##############################
RETURN:
        # hx_grid_supply_temperature  [ºC]
        # hx_grid_target_temperature  [ºC]
        # hx_sink_supply_temperature  [ºC]
        # hx_sink_target_temperature  [ºC]


"""


def sink_get_hx_temperatures(grid_supply_temperature, grid_return_temperature, stream_supply_temperature, stream_target_temperature, hx_delta_T):

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
