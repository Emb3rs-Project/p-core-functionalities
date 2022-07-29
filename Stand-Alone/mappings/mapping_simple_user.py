

def mapping_simple_user(_sink_raw, user_type):

    mapped_data = {
                    "platform": {
                        "type_of_object": user_type,
                        "name": _sink_raw["name"],
                        "location": _sink_raw["location"],
                        "streams": _sink_raw["raw_streams"]}
                    }

    return mapped_data