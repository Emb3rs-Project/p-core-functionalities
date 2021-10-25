import copy

def sink_data_pre_treatment(group_sink,group_type):

    output = []
    hot_grid_delta_T = 30
    cold_grid_delta_T = 2
    min_hot_grid_temperature = 20
    group_grid_sink_supply_temperature = -10  # safety
    group_grid_sink_return_temperature = -10  # safety
    group_sink_supply_capacity = -10  # safety
    group_sink_yearly_capacity = 0

    for sink in group_sink:
        new_grid_sink_supply_temperature = sink['grid_sink_supply_temperature']
        new_grid_sink_return_temperature = sink['grid_sink_return_temperature']
        new_group_sink_supply_capacity = sink['max_capacity']

        if group_type == 'heating':
            if new_grid_sink_supply_temperature > group_grid_sink_supply_temperature:
                group_grid_sink_supply_temperature = copy.copy(new_grid_sink_supply_temperature)

            if new_grid_sink_return_temperature > group_grid_sink_return_temperature:
                group_grid_sink_return_temperature = copy.copy(new_grid_sink_return_temperature)

            if new_group_sink_supply_capacity > group_sink_supply_capacity:
                group_sink_supply_capacity = copy.copy(new_group_sink_supply_capacity)

            group_sink_yearly_capacity += sum(sink['corrected_hourly_sink_capacity'])  # [kWh]
        else:
            if new_grid_sink_supply_temperature < group_grid_sink_supply_temperature:
                group_grid_sink_supply_temperature = copy.copy(new_grid_sink_supply_temperature)

            if new_grid_sink_return_temperature > group_grid_sink_supply_temperature:
                group_grid_sink_return_temperature = copy.copy(new_grid_sink_return_temperature)

            if new_group_sink_supply_capacity > group_sink_supply_capacity:
                group_sink_supply_capacity = copy.copy(new_group_sink_supply_capacity)

            group_sink_yearly_capacity += sum(sink['corrected_hourly_sink_capacity'])  # [kWh]


    if group_grid_sink_supply_temperature != -10 and group_grid_sink_return_temperature != -10 and group_sink_supply_capacity != -10:
        # Compute grid supply and return on the sink side
        if group_grid_sink_supply_temperature >= min_hot_grid_temperature:  # Oil/Hot DHN
            delta_T = hot_grid_delta_T  # defined grid delta_T  on sink side
            grid_sink_supply_temperature = group_grid_sink_supply_temperature

            if group_grid_sink_supply_temperature - group_grid_sink_return_temperature > delta_T:
                grid_sink_return_temperature = group_grid_sink_return_temperature
            else:
                grid_sink_return_temperature = group_grid_sink_return_temperature
                grid_sink_supply_temperature = grid_sink_return_temperature + delta_T

        else:  # Cold DHN
            delta_T = cold_grid_delta_T  # defined grid delta_T  on sink side
            grid_sink_supply_temperature = group_grid_sink_supply_temperature
            if group_grid_sink_return_temperature > group_grid_sink_supply_temperature + delta_T:
                grid_sink_return_temperature = group_grid_sink_return_temperature
            else:
                grid_sink_return_temperature = group_grid_sink_return_temperature
                grid_sink_supply_temperature = grid_sink_return_temperature - delta_T

        output = {
                  'group_sink_yearly_capacity': group_sink_yearly_capacity,
                  'group_grid_sink_return_temperature':grid_sink_return_temperature,
                  'group_grid_sink_supply_temperature':grid_sink_supply_temperature,
                  'group_sink_supply_capacity':group_sink_supply_capacity
        }

    return output