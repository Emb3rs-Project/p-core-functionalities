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
        schedule - vector with 1 and 0 // default:None
        hourly_generation - [kWh] // default:None


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
            #         'monthly_generation': monthly_generation  # [kWh]
            #         'capacity'  [kW]
            #     }

"""

from random import randint


months = [
    "january"
    , "february"
    , "march"
    , "april"
    , "may"
    , "june"
    , "july"
    , "august"
    , "september"
    , "october"
    , "november"
    , "december"
]

def stream_industry(stream_name,object_linked_id, stream_type, fluid, supply_temperature, target_temperature, mass_flowrate, capacity,
                    schedule=None, hourly_generation=None, stream_id=None):


    if stream_id == None:
        raise Exception('No stream ID given. Report to the platform.')

    if hourly_generation is None:
        hourly_generation = [i * capacity for i in schedule]
    else:
        schedule = list(map(lambda x: 1 if x > 0 else 0, hourly_generation))


    i = 48  # repeat last day
    hours_needed = 366*24-1
    if len(hourly_generation) < hours_needed:
        while len(hourly_generation) != hours_needed:
            hourly_generation.append(hourly_generation[-i])
            schedule.append(schedule[-i])
            i += 1
    else:
        hourly_generation = hourly_generation[:hours_needed]
        schedule = schedule[:hours_needed]


    # get monthly generation
    hour_new_month = 0
    monthly_generation = []
    for index, month in enumerate(months):
        if month == 'january' or month =='march' or month =='may' or month =='july' or month =='august' or month =='october' or month =='december':
            number_days = 31
        elif month == 'february':
            number_days = 29  # year with 366 days considered
        else:
            number_days = 30

        initial = hour_new_month
        final = hour_new_month + number_days * 24


        if month != 'december':
            monthly_generation.append(sum(hourly_generation[initial:final]))
        else:

            monthly_generation.append(sum(hourly_generation[initial:]))

        hour_new_month = final

    stream_data = {
        'name': stream_name,
        'id': stream_id,
        'object_type': 'stream',
        'object_linked_id': object_linked_id,  # Object ID associated; e.g. process or equipment ID
        'stream_type': stream_type,  # e.g. inflow, supply_heat, excess_heat
        'supply_temperature': supply_temperature,  # T_in  # [ºC]
        'target_temperature': target_temperature,  # T_out  # [ºC]
        'fluid': fluid,
        'flowrate': mass_flowrate,  # [kg/h]
        'schedule': schedule,  # array with 1 and 0
        'hourly_generation': hourly_generation,  # [kWh]
        'capacity': capacity,  # [kW]
        'monthly_generation': monthly_generation  # [kWh]
    }

    return stream_data
