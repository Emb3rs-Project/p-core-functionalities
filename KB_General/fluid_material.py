"""
@author: jmcunha/alisboa

Info: Fluids and materials properties

"""
import json

def fluid_material_cp(fluid_name,temperature):

    with open('Json_files/medium_list.json') as f:
        data = json.load(f)

    try:
        fluid_cp = data[fluid_name]['specific_heat_c0'] + data[fluid_name]['specific_heat_c1'] * temperature \
                   + data[fluid_name]['specific_heat_c2'] * temperature**2 + data[fluid_name]['specific_heat_c3'] * temperature**3

    except:
        print('fluid does not exist in db. fluid_cp = 1')
        fluid_cp = 1


    return fluid_cp



def fluid_material_rho(fluid_name,temperature):

    with open('Json_files/medium_list.json') as f:
        data = json.load(f)

    try:
        rho = data[fluid_name]['density_c0'] + data[fluid_name]['density_c1'] * temperature \
                   + data[fluid_name]['density_c2'] * temperature ** 2 + data[fluid_name][
                       'density_c3'] * temperature ** 3

    except:
        print('fluid does not exist in db. rho = 1')
        rho = 1

    return rho


def fluid_material_state(fluid_name):

    with open('Json_files/medium_list.json') as f:
        data = json.load(f)

    try:
        state = data[fluid_name]['fluid_type']

    except:
        print('fluid does not exist in db. rho = 1')
        state = 'liquid'

    return state

