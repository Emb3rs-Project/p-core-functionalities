"""
alisboa/jmcunha


##############################
INFO: compute temperatures for the HX between source and grid


##############################
INPUT:
        # hx_grid_stream_target_temperature  [ºC]
        # hx_grid_stream_supply_temperature [ºC]
        # source_stream_supply_temperature [ºC]
        # source_stream_target_temperature [ºC]
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
