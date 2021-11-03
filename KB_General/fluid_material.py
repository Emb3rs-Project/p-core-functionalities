"""
@author: jmcunha/alisboa

Info: Fluids and materials properties

"""
import json
import os

def fluid_material_cp(fluid_name,temperature):

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","medium_list.json" )

    with open(abs_file_path) as f:
        data = json.load(f)

    try:
        fluid_cp = float(data[fluid_name]['specific_heat_c0']) + float(data[fluid_name]['specific_heat_c1']) * temperature \
                   + float(data[fluid_name]['specific_heat_c2']) * temperature**2 + float(data[fluid_name]['specific_heat_c3']) * temperature**3

    except:
        print('fluid does not exist in db. fluid_cp = 1')
        fluid_cp = 1

    return fluid_cp



def fluid_material_rho(fluid_name,temperature):

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","medium_list.json" )

    with open(abs_file_path) as f:
        data = json.load(f)

    try:
        rho = float(data[fluid_name]['density_c0']) + float(data[fluid_name]['density_c1']) * temperature \
                   + float(data[fluid_name]['density_c2']) * temperature ** 2 + float(data[fluid_name][
                       'density_c3']) * temperature ** 3

    except:
        print('fluid does not exist in db. rho = 1')
        rho = 1

    return rho


def fluid_material_state(fluid_name):

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","medium_list.json" )

    with open(abs_file_path) as f:
        data = json.load(f)

    try:
        state = data[fluid_name]['fluid_type']

    except:
        print('fluid does not exist in db. rho = 1')
        state = 'liquid'

    return state

