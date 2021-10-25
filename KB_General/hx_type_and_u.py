"""
@author: jmcunha/alisboa

Info: Receive Fluid type and return appropriate heat exchanger and U value [W/m2.K]

Return: [hx_type,hx_u_value]
"""

import json


def hx_type_and_u(fluid_1,fluid_2):

    with open('./Json_files/medium_list.json') as f:
        data = json.load(f)

    try:
        state_1 = data[fluid_1]['fluid_type']
    except:
        print('fluid does not exist in db. state = liquid')
        state_1 = 'liquid'

    try:
        state_2 = data[fluid_2]['fluid_type']
    except:
        print('fluid does not exist in db. state = liquid')
        state_2 = 'liquid'

    if state_1 == 'liquid' and state_2 == 'liquid':
        hx_type = 'hx_plate'
        hx_u_value = 2000

    elif (state_1 == 'flue_gas' and state_2 == 'liquid') or (state_1 == 'liquid' and state_2 == 'flue_gas'):
        hx_type = 'hx_economizer'
        hx_u_value = 50

    elif (state_1 == 'liquid' and state_2 == 'steam') or (state_1 == 'steam' and state_2 == 'liquid'):
        hx_type = 'hx_kettle_boiler'
        hx_u_value = 800

    else:
        print('combination of liquids not in db')
        hx_type = 'hx_plate'
        hx_u_value = 800

    return hx_type,hx_u_value

