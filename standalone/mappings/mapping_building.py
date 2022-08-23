
def mapping_building(data):

    mapped_data = {
        "platform": {
            "location": data["location"]}
    }
    mapped_data["platform"].update(data["info"])

    return mapped_data