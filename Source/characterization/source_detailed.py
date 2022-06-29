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
from ...General.Simple_User.isolated_stream import isolated_stream
from ...utilities.kb import KB
from ...Error_Handling.error_source_detailed import error_source_detailed
from ...Error_Handling.runtime_error import ModuleRuntimeException


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
    index_to_pop = []

    try:
        for index, object_info in enumerate(platform_data):
            print(object_info)
            if object_info['object_type'] == 'process':
                new_process = Process(object_info, kb)
                objects_list.append(new_process)
                processes_data[str(new_process.id)] = new_process
                index_to_pop.append(index)
    except:
        raise ModuleRuntimeException(
            code="1",
            type="source_detailed.py",
            msg="Process object creation infeasible. Please check your inputs. \n "
                "If all inputs are correct report to the platform.")


    index_to_pop.sort(reverse=True)
    for i in index_to_pop:
        platform_data.pop(i)

    # EQUIPMENT
    index_to_pop = []
    for index, equipment_info in enumerate(platform_data):
        equipment_info['processes'] = []

        #if equipment_info['processes_id'] is not None:
        #    for process_id in equipment_info['processes_id']:
        #        equipment_info['processes'].append(processes_data[str(process_id)])
#
        #    equipment_info['processes'] = [vars(process) for process in equipment_info['processes']]

        if equipment_info['object_type'] == 'boiler' or equipment_info['object_type'] == 'chp' or equipment_info['object_type'] == 'burner' or equipment_info['object_type'] == 'cooling_equipment':

            if equipment_info['object_type'] == 'boiler':
                new_equipment = Boiler(equipment_info, kb)
            elif equipment_info['object_type'] == 'chp':
                new_equipment = Chp(equipment_info, kb)
            elif equipment_info['object_type'] == 'burner':
                new_equipment = Burner(equipment_info, kb)
            elif equipment_info['object_type'] == 'cooling_equipment':
                new_equipment = Cooling_Equipment(equipment_info, kb)

            index_to_pop.append(index)
            objects_list.append(new_equipment)

    # remove equipment from list
    index_to_pop.sort(reverse=True)
    for i in index_to_pop:
        platform_data.pop(i)

    # STREAM
    for index, stream_info in enumerate(platform_data):
        isolated_stream_output = isolated_stream([stream_info])
        new_object = isolated_stream_output['streams'][0]
        objects_list.append(new_object)

    # give IDs to streams
    index_stream = 1
    for object in objects_list:

        try:
            for stream in object.streams:
                stream["id"] = index_stream
                index_stream += 1
        except:
            print(object)
            object["id"] = index_stream
            index_stream += 1

    return objects_list
