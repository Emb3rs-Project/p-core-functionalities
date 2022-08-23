

def mapping_convert_sources(sources):

    data ={
            "platform": {"group_of_sources":sources},
            "cf_module": {"sink_group_grid_supply_temperature": 90,
                          "sink_group_grid_return_temperature": 60}
    }


    return data