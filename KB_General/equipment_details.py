"""
alisboa/jmcunha


##############################
INFO: It were created correlations for the turnkey, om_fix, and equipment efficiency based on the various info from suppliers
      and the literature. In this script, these equipment characteristics are obtained according to its characteristic parameter
      (e.g., boilers - power [kW]; hx_plate - area [m2],...)


##############################
INPUT:
        # equipment - equipment name
        # equipment_char -  characteristic parameter of the equipment


##############################
OUTPUT:
        # global_conversion_efficiency  []
        # om_fix  [€/kW]
        # turnkey  [€]


"""

import json
import os


def equipment_details(equipment, equipment_char):

    global_conversion_efficiency = 1
    electrical_conversion_efficiency = 1
    om_fix = 1
    turnkey = 1

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files", "equipment_details.json")

    with open(abs_file_path) as f:
        data = json.load(f)

    try:
        turnkey = float(data[equipment]['turnkey_cost_S']) + float(
            data[equipment]['turnkey_cost_c']) * equipment_char ** float(data[equipment]['turnkey_cost_n'])
        om_fix = float(data[equipment]['fixed_om_c']) * turnkey ** float(data[equipment]['fixed_om_n'])
        global_conversion_efficiency = float(data[equipment]['global_conversion_efficiency_S']) + float(
            data[equipment]['global_conversion_efficiency_c']) * equipment_char ** float(
            data[equipment]['global_conversion_efficiency_n'])
        electrical_conversion_efficiency = float(data[equipment]['electrical_efficiency_c']) * equipment_char ** float(
            data[equipment]['electrical_efficiency_n'])
    except:
        print('equipment not in db. script: equipment_details')

    # special case CHP
    if equipment == 'chp_gas_engine' or equipment == 'chp_gas_turbine':
        global_conversion_efficiency = [global_conversion_efficiency, electrical_conversion_efficiency]  # thermal and electrical efficiency

    return global_conversion_efficiency, om_fix, turnkey
