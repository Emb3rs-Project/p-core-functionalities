"""
##############################
INFO: 'Template' to create stream.

##############################
INPUT:  object_linked_id - Object ID associated; e.g. process or equipment ID
        stream_type - e.g. inflow, supply_heat, excess_heat
        fluid - fluid
        supply_temperature [ºC]
        target_temperature [ºC]
        mass_flowrate [kg/h]
        capacity  [kW]
        schedule - vector with 1 and 0

##############################
OUTPUT:  stream dictionary, as below:
            #  stream_data = {
            #         'id',
            #         'object_type' - e.g. 'stream',
            #         'object_linked_id' - Object ID associated; e.g. process or equipment ID
            #         'stream_type',  - e.g. inflow, supply_heat, excess_heat
            #         'supply_temperature',  [ºC]
            #         'target_temperature',  [ºC]
            #         'fluid',
            #         'flowrate'   [kg/h]
            #         'schedule' -  array with 1 and 0
            #         'hourly_generation' [kWh]
            #         'capacity'  [kW]
            #     }

"""

from random import randint


def stream_industry(object_linked_id, stream_type, fluid, supply_temperature, target_temperature, mass_flowrate, capacity,
                    schedule=None, hourly_generation=None):

    if hourly_generation is None:
        hourly_generation = [i * capacity for i in schedule]
    else:
        schedule = list(map(lambda x: 1 if x > 0 else 0, hourly_generation))

    i = 24  # repeat last day
    while len(hourly_generation) != 366*24:
        hourly_generation.append(hourly_generation[-(i):])
        schedule.append(schedule[-(i):])
        i +=1


    stream_data = {
        'id': randint(0, 10 ** 5),
        'object_type': 'stream',
        'object_linked_id': object_linked_id,  # Object ID associated; e.g. process or equipment ID
        'stream_type': stream_type,  # e.g. inflow, supply_heat, excess_heat
        'supply_temperature': supply_temperature,  # T_in  # [ºC]
        'target_temperature': target_temperature,  # T_out  # [ºC]
        'fluid': fluid,
        'flowrate': mass_flowrate,  # [kg/h]
        'schedule': schedule,  # array with 1 and 0
        'hourly_generation': hourly_generation,  # [kWh]
        'capacity': capacity  # [kW]
    }

    return stream_data
