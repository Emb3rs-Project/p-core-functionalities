"""
##############################
INFO: Source detailed User - User that characterizes both processes and equipment. Receives a list with the data needed
to create each object (process,boiler,chp,burner,cooling equipment) and returns a list with the objects created.

##############################
INPUT: list with dicts with each object data -> Check inputs in process, generate_boiler, generate_chp,
generate_cooling_equipment, process, generate_boiler, generate_burner

##############################
OUTPUT:  list with objects -> Check attributes in process, generate_boiler, generate_chp, generate_cooling_equipment,
process, generate_boiler, generate_burner

"""

from .Process.process import Process
from .Generate_Equipment.generate_cooling_equipment import Cooling_Equipment
from .Generate_Equipment.generate_chp import Chp
from .Generate_Equipment.generate_boiler import Boiler
from .Generate_Equipment.generate_burner import Burner
from ...utilities.kb import KB
from ...Error_Handling.error_source_detailed import error_source_detailed

def source_detailed(in_var, kb: KB):
    #################
    # INPUT
    # Validate Inputs
    platform_data = error_source_detailed(in_var['platform'])

    #################
    # Get objects
    objects_list = []  # process + equipment
    processes_data = {}

    # create processes
    for index, object_info in enumerate(platform_data):
        if object_info['object_type'] == 'process':
            new_process = Process(object_info, kb)
            objects_list.append(new_process)
            processes_data[str(new_process.id)] = new_process
            platform_data.pop(index)




    # create equipment
    for index, equipment_info in enumerate(platform_data):

        equipment_info['processes'] = []

        if equipment_info['processes_id'] is not None:
            for process_id in equipment_info['processes_id']:
                equipment_info['processes'].append(processes_data[str(process_id)])


        if equipment_info['object_type'] == 'boiler':
            new_equipment = Boiler(equipment_info, kb)
        elif equipment_info['object_type'] == 'chp':
            new_equipment = Chp(equipment_info, kb)
        elif equipment_info['object_type'] == 'burner':
            new_equipment = Burner(equipment_info, kb)
        elif equipment_info['object_type'] == 'cooling_equipment':
            new_equipment = Cooling_Equipment(equipment_info, kb)

        objects_list.append(new_equipment)

    return objects_list
