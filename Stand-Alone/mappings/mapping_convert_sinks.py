
def mapping_convert_sinks(sinks):

    data ={
            "platform": {"group_of_sinks":sinks,
                         "grid_supply_temperature": 90,
                         "grid_return_temperature": 60
                        }

    }

    return data