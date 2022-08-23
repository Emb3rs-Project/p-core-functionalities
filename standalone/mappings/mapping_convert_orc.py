def mapping_convert_orc(fuels_data,
                        simple_sources_data,
                        orc_data):

    data = {
        "platform": {
            "streams": simple_sources_data[0]["streams"],  # only one source should be sent to ORC analysis
            "get_best_number": 3,
            "orc_years_working": orc_data["orc_years_working"],
            "orc_T_evap": orc_data["orc_T_evap"],
            "orc_T_cond": orc_data["orc_T_cond"],
            "fuels_data": fuels_data,
            "interest_rate": orc_data["interest_rate"],
            "location" : simple_sources_data[0]['location']
        }
    }

    return data
