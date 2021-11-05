"""
INFO: Pumping - [m3/h] to [kW]  from KB_General

INPUT: Flowrate in [kg/h]

OUTPUT: Power in [kW]

"""

import json
import os

def flowrate_to_power(flowrate):

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files", "equipment_details.json")

    with open(abs_file_path) as f:
        data = json.load(f)

    pumping_power_c = float(data['circulation_pumping']['pumping_power_c'])
    pumping_power_n = float(data['circulation_pumping']['pumping_power_n'])

    return pumping_power_c * (flowrate) ** (pumping_power_n)  # [m3/h] to [kW]  from KB_General


