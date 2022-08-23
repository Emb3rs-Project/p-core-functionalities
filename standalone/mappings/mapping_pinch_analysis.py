

def mapping_pinch_analysis(cf_data):
    data = {"platform": {"streams": cf_data['sources'][0]['raw_streams'],
                         "pinch_delta_T_min": cf_data['pinch_data']["pinch_delta_T_min"],
                         "fuels_data": cf_data['fuels_data'],
                         "streams_to_analyse": cf_data['pinch_data']["streams_to_analyse"],
                         "interest_rate":cf_data['pinch_data']["interest_rate"]}
    }

    return data

