"""
alisboa/jmcunha


##############################
INFO: compute for the hx between source and grid, its temperatures, according to the source's streams temperature needs
      and the grid temperatures


##############################
INPUT:
        # defined_stream_supply_temperature  [ºC]
        # defined_stream_return_temperature  [ºC]
        # stream_supply_temperature  [ºC]
        # stream_target_temperature  [ºC]
        # hx_delta_T   [ºC]


##############################
RETURN:
        # hx_defined_stream_supply_temperature  [ºC]
        # hx_defined_stream_target_temperature  [ºC]
        # hx_undefined_stream_supply_temperature  [ºC]
        # hx_undefined_stream_target_temperature  [ºC]


"""


def source_get_hx_temperatures(defined_stream_supply_temperature, defined_stream_return_temperature,stream_supply_temperature,
                               stream_target_temperature, hx_delta_T):

    hx_defined_stream_supply_temperature = defined_stream_supply_temperature
    hx_defined_stream_target_temperature = defined_stream_return_temperature
    hx_undefined_stream_supply_temperature = stream_supply_temperature

    if stream_target_temperature > defined_stream_supply_temperature + hx_delta_T and stream_supply_temperature > defined_stream_return_temperature + hx_delta_T:
        hx_undefined_stream_target_temperature = stream_target_temperature

    else:  # stream_target_temperature < defined_stream_supply_temperature + hx_delta_T:
        hx_undefined_stream_target_temperature = defined_stream_return_temperature + hx_delta_T

    return hx_defined_stream_supply_temperature, hx_defined_stream_target_temperature, hx_undefined_stream_supply_temperature, hx_undefined_stream_target_temperature
