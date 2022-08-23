
def mapping_convert_sinks(sinks,grid_supply_temperature, grid_return_temperature):

    data ={
            "platform": {"group_of_sinks":sinks,
                         "grid_supply_temperature": grid_supply_temperature,
                         "grid_return_temperature": grid_return_temperature
                        }

    }

    return data