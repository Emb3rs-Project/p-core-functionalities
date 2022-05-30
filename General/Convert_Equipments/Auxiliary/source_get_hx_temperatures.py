"""
alisboa/jmcunha


##############################
INFO: compute for the hx between source and grid, its temperatures, according to the source's streams temperature needs
      and the grid temperatures


##############################
INPUT:
        # grid_stream_supply_temperature  [ºC]
        # grid_stream_return_temperature  [ºC]
        # stream_supply_temperature  [ºC]
        # stream_target_temperature  [ºC]
        # hx_delta_T   [ºC]


##############################
RETURN:
        # hx_grid_stream_supply_temperature  [ºC]
        # hx_grid_stream_target_temperature  [ºC]
        # hx_source_stream_supply_temperature  [ºC]
        # hx_source_stream_target_temperature  [ºC]


"""


def source_get_hx_temperatures(hx_grid_stream_target_temperature, hx_grid_stream_supply_temperature,source_stream_supply_temperature,
                               source_stream_target_temperature, hx_delta_T):

    hx_source_stream_supply_temperature = source_stream_supply_temperature

    # if source stream target_temperature > hx_grid
    if source_stream_target_temperature > hx_grid_stream_supply_temperature + hx_delta_T:
        hx_source_stream_target_temperature = source_stream_target_temperature

    else:  # stream_target_temperature < grid_stream_supply_temperature + hx_delta_T:
        hx_source_stream_target_temperature = hx_grid_stream_supply_temperature + hx_delta_T

        if hx_source_stream_target_temperature < source_stream_target_temperature:
            hx_source_stream_target_temperature = source_stream_target_temperature




    return hx_grid_stream_supply_temperature, hx_grid_stream_target_temperature, hx_source_stream_supply_temperature, hx_source_stream_target_temperature
