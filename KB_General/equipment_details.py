import json

def equipment_details(equipment,equipment_char):

    global_conversion_efficiency = 0
    electrical_conversion_efficiency = 0
    om_fix = 0
    turnkey = 0

    with open('C:/Users/alisboa/PycharmProjects/emb3rs/KB_General/Json_files/equipment_details.json') as f:
        data = json.load(f)

    for dict in data['equipment_details']:
        if dict['equipment'] == equipment:
            om_fix = float(dict['fixed_om_c']) * equipment_char ** float(dict['fixed_om_n'])
            turnkey = float(dict['turnkey_cost_S']) + float(dict['turnkey_cost_c']) * equipment_char ** float(dict['turnkey_cost_n'])
            global_conversion_efficiency = float(dict['global_conversion_efficiency_S']) + float(dict['global_conversion_efficiency_c']) * equipment_char ** float(dict['global_conversion_efficiency_n'])
            electrical_conversion_efficiency = float(dict['electrical_efficiency_c']) * equipment_char ** float(dict['electrical_efficiency_n'])
            break

    if equipment == 'chp_gas_engine' or equipment == 'chp_gas_turbine':
        global_conversion_efficiency = [global_conversion_efficiency, electrical_conversion_efficiency]  # thermal and electrical

    return global_conversion_efficiency,om_fix,turnkey



