
"""
UPDATE ERROR HANDLING JSONs

"""

import requests
import json

sheets_name = ['building', 'greenhouse', 'sink_adjust_capacity', 'convert_sinks', 'group_of_sinks', 'streams',
               'stream_building']

for sheet in sheets_name:
    url = "https://opensheet.elk.sh/1T5QHmNIATsaAxaFkjnLdC4PiMz3PTzhTD1fc0xReOLc/" + sheet
    file_json = requests.get(url).json()

    dict = {}
    for parameter in file_json:
        if parameter["options"] != '-':

            array = parameter["options"].split(";")
            parameter["options"] = []
            for val in array:
                if val.isnumeric() is True:
                    val = int(val)
                    parameter["options"].append(val)
                elif val == 'null':
                    parameter["options"] = None
                else:
                    parameter["options"].append(val)

        else:
            parameter["options"] = []

        dict[str(parameter['var name'])] = parameter


    with open('labels_var/' + sheet + '.json', 'w') as outfile:
        json.dump(dict, outfile)

