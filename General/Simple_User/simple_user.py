"""
##############################
INFO: Simple User streams characterization.

##############################
INPUT: object with:

        # id
        # type_of_object - 'sink' or 'source'
        # streams -> vector with dictionaries

        Where in streams:
         # supply_temperature [ºC]
         # target_temperature [ºC]
         # fluid - name
         # fluid_cp [kJ/kg.K]
         # flowrate [kg/h]
         # saturday_on - 1 (yes)  or 0 (no)
         # sunday_on - 1 (yes)  or 0 (no)
         # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
         # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]

##############################
OUTPUT: vector with dictionaries:

        # id - stream id
        # object_type - stream
        # object_id - # Object ID associated; e.g. process or equipment ID
        # fluid - water
        # stream_type - inflow
        # schedule - 1 and 0 profile
        # hourly_generation - array [kWh]
        # capacity [kW]
        # supply_temperature [ºC]
        # target_temperature [ºC]

"""

from ...General.Auxiliary_General.stream_industry import stream_industry
from ...General.Auxiliary_General.schedule_hour import schedule_hour
import json

def simple_user(in_var):

        # INPUT  ------------------------
        object_id = in_var.object_id
        type_of_object = in_var.type_of_object
        streams = in_var.streams

        # Defined vars
        if type_of_object == 'sink':
            stream_type = 'inflow'
        else:
            stream_type = 'excess_heat'

        streams_output = []

        # COMPUTE ------------------------
        for stream in streams:
                capacity = stream['flowrate'] * stream['fluid_cp'] * abs(( stream['supply_temperature'] - stream['target_temperature']))/3600  # [kW]
                schedule = schedule_hour(stream['saturday_on'], stream['sunday_on'], stream['shutdown_periods'], stream['daily_periods'])
                info_stream = stream_industry(object_id,stream_type,stream['fluid'],stream['supply_temperature'],stream['target_temperature'],stream['flowrate'],capacity,schedule)
                streams_output.append(info_stream)

        # OUTPUT ------------------------
        output = {'streams':streams}

        #output = json.dumps(output, indent=2)

        return output



