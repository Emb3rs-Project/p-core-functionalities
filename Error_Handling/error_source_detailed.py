from pydantic import BaseModel
from typing import List
from .Source_Detail.source_detailed_object import SourceDetailedObject
from .Source_Detail.boiler import Boiler
from .Source_Detail.process import Process
from .Source_Detail.burner import Burner
from .Source_Detail.cooling_equipment import CoolingEquipment
from .Source_Detail.chp import Chp


class PlatformSourceDetailed(BaseModel):
    all_objects_info: List[SourceDetailedObject]


def error_source_detailed(platform_data):
    # first input validation
    PlatformSourceDetailed(**platform_data)

    data = []
    processes_equipment_id = []  # equipment ID associated to processes list
    equipments_process_id = []  # process ID associated to equipment list
    equipment_id = []
    index_to_pop = []
    all_objects_info = platform_data["all_objects_info"]

    # check processes
    for i_object_source, object_source in enumerate(all_objects_info):
        if object_source['object_type'] == 'process':
            new_process = Process(**object_source)  # process input validation
            new_process.inflow_data = [vars(i) for i in new_process.inflow_data]
            new_process.outflow_data = [vars(i) for i in new_process.outflow_data]
            new_process.startup_data = [vars(i) for i in new_process.startup_data]
            new_process.maintenance_data = [vars(i) for i in new_process.maintenance_data]

            # get process
            new_process = vars(new_process)
            data.append(new_process)
            processes_equipment_id.append(new_process['equipment_id'])
            index_to_pop.append(i_object_source)

    for i in index_to_pop:
        all_objects_info.pop(i)

    # check equipment
    for i_equipment, equipment in enumerate(all_objects_info):
        if equipment['object_type'] == 'boiler':
            new_equipment = Boiler(**equipment)
        elif equipment['object_type'] == 'chp':
            new_equipment = Chp(**equipment)
        elif equipment['object_type'] == 'burner':
            new_equipment = Burner(**equipment)
        elif equipment['object_type'] == 'cooling_equipment':
            new_equipment = CoolingEquipment(**equipment)
        equipment_id.append(equipment['id'])

        try:
            for i in equipment['processes_id']:
                equipments_process_id.append(i)
        except:
            pass

        data.append(vars(new_equipment))



##########################


    for process_equipment_id in processes_equipment_id:
        if process_equipment_id not in equipment_id:
            raise Exception('A process is associated with an incorrect equipment ID.')

    for equipment_process_id in equipments_process_id:
        if equipment_process_id not in processes_equipment_id:
            raise Exception('An equipment is associated with an incorrect process ID.')

    return data
