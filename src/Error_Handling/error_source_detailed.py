"""
alisboa/jmcunha


##############################
INFO: Source detailed (equipment+processes+unique streams) error handling


"""

from pydantic import BaseModel
from typing import List
from .Source_Detail.source_detailed_object import SourceDetailedObject
from .Source_Detail.boiler import Boiler
from .Source_Detail.process import Process
from .Source_Detail.burner import Burner
from .Source_Detail.cooling_equipment import CoolingEquipment
from .Source_Detail.chp import Chp
from .error_isolated_stream import StreamData


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

            if new_process.inflow_data != None:
                new_process.inflow_data = [vars(i) for i in new_process.inflow_data]
            if new_process.outflow_data != None:
                new_process.outflow_data = [vars(i) for i in new_process.outflow_data]
            if new_process.maintenance_data != None:
                new_process.maintenance_data = [vars(i) for i in new_process.maintenance_data]

            # get process
            new_process = vars(new_process)
            data.append(new_process)
            processes_equipment_id.append(new_process['equipment_id'])
            index_to_pop.append(i_object_source)

    # remove processes from list
    index_to_pop.sort(reverse=True)
    for i in index_to_pop:
        all_objects_info.pop(i)

    # check equipment
    index_to_pop = []
    for i_equipment, equipment in enumerate(all_objects_info):
        if equipment['object_type'] == 'boiler' or equipment['object_type'] == 'chp' or equipment[
            'object_type'] == 'burner' or equipment['object_type'] == 'cooling_equipment':
            if equipment['object_type'] == 'boiler':
                new_equipment = Boiler(**equipment)
            elif equipment['object_type'] == 'chp':
                new_equipment = Chp(**equipment)
            elif equipment['object_type'] == 'burner':
                new_equipment = Burner(**equipment)
            elif equipment['object_type'] == 'cooling_equipment':
                new_equipment = CoolingEquipment(**equipment)

            equipment_id.append(equipment['id'])
            index_to_pop.append(i_equipment)

            try:
                for i in equipment['processes_id']:
                    equipments_process_id.append(i)
            except:
                pass

            data.append(vars(new_equipment))

    # remove equipment from list
    index_to_pop.sort(reverse=True)
    for i in index_to_pop:
        all_objects_info.pop(i)

    # check unique streams - stream by stream
    for i_stream, stream in enumerate(all_objects_info):
        if stream['object_type'] == 'stream':
            stream_ = StreamData(**stream)
            data.append(vars(stream_))

    ##########################
    for process_equipment_id in processes_equipment_id:
        if process_equipment_id not in equipment_id:
            raise Exception('A process is associated with an incorrect equipment ID.')

    return data
