

def stream_industry(object_id,stream_type,fluid,supply_temperature,target_temperature,mass_flowrate,capacity,schedule):
        stream_data = {
            'id':0,
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

