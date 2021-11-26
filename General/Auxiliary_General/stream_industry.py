"""
##############################
INFO: 'Template' to create stream.

##############################
INPUT:  object_id - Object ID associated; e.g. process or equipment ID
        stream_type - e.g. inflow, supply_heat, excess_heat
        fluid - fluid
        supply_temperature [ºC]
        target_temperature [ºC]
        mass_flowrate [kg/h]
        capacity  [kW]
        schedule - vector with 1 and 0

##############################
OUTPUT:  stream dictionary with:
            # id
            # object_type - stream
            # object_id - Object ID associated; e.g. process or equipment ID
            # stream_type - e.g. inflow, supply_heat, excess_heat
            # supply_temperature  [ºC]
            # target_temperature  [ºC]
            # fluid - fluid,
            # flowrate  [kg/h]
            # schedule - vector with 1 and 0
            # hourly_generation  [kWh]
            # capacity  [kW]


"""


from random import randint

def stream_industry(object_id,stream_type,fluid,supply_temperature,target_temperature,mass_flowrate,capacity,schedule):
        stream_data = {
            'id':randint(0,10**5),
            'object_type':'stream',
            'object_id':object_id,  # Object ID associated; e.g. process or equipment ID
            'stream_type':stream_type,  # e.g. inflow, supply_heat, excess_heat
            'supply_temperature':supply_temperature,  # T_in  # [ºC]
            'target_temperature':target_temperature,  # T_out  # [ºC]
            'fluid':fluid,
            'flowrate':mass_flowrate,  # [kg/h]
            'schedule':schedule,  # vector with 1 and 0
            'hourly_generation':[i * capacity for i in schedule],  # [kWh]
            'capacity':capacity  # [kW]
            }

        return stream_data

