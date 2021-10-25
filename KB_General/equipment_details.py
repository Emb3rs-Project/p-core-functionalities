import json

def equipment_details(equipment,equipment_char):

    global_conversion_efficiency = 1
    electrical_conversion_efficiency = 1
    om_fix = 1
    turnkey = 1

    with open('Json_files/equipment_details.json') as f:
        data = json.load(f)

    try:
        om_fix = float(data[equipment]['fixed_om_c']) * equipment_char ** float(data[equipment]['fixed_om_n'])
        turnkey = float(data[equipment]['turnkey_cost_S']) + float(data[equipment]['turnkey_cost_c']) * equipment_char ** float(data[equipment]['turnkey_cost_n'])
        global_conversion_efficiency = float(data[equipment]['global_conversion_efficiency_S']) + float(data[equipment]['global_conversion_efficiency_c']) * equipment_char ** float(data[equipment]['global_conversion_efficiency_n'])
        electrical_conversion_efficiency = float(data[equipment]['electrical_efficiency_c']) * equipment_char ** float(data[equipment]['electrical_efficiency_n'])
    except:
        print('equipment not in db')


    if equipment == 'chp_gas_engine' or equipment == 'chp_gas_turbine':
        global_conversion_efficiency = [global_conversion_efficiency, electrical_conversion_efficiency]  # thermal and electrical

    return global_conversion_efficiency,om_fix,turnkey



