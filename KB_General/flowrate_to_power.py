"""
alisboa/jmcunha


##############################
INFO: Computes power needed for the given flowrate


##############################
INPUT:
        # flowrate  [kg/h]


##############################
OUTPUT:
        # power  [kW]


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

    power = pumping_power_c * flowrate ** pumping_power_n  # [kg/h] to [kW]

    return power
