
def source_get_hx_temperatures(defined_stream_supply_temperature ,defined_stream_return_temperature ,stream_supply_temperature,stream_target_temperature ,hx_delta_T):

    hx_defined_stream_supply_temperature = defined_stream_supply_temperature
    hx_defined_stream_target_temperature = defined_stream_return_temperature
    hx_undefined_stream_supply_temperature = stream_supply_temperature

    if stream_target_temperature > defined_stream_supply_temperature + hx_delta_T and stream_supply_temperature > defined_stream_return_temperature + hx_delta_T:
        hx_undefined_stream_target_temperature = stream_target_temperature

    else:  # stream_target_temperature < defined_stream_supply_temperature + hx_delta_T:
        hx_undefined_stream_target_temperature = defined_stream_supply_temperature + hx_delta_T

    return hx_defined_stream_supply_temperature, hx_defined_stream_target_temperature, hx_undefined_stream_supply_temperature, hx_undefined_stream_target_temperature