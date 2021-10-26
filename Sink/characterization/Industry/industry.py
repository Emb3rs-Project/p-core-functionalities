"""
##############################
INFO: Sink Industry streams characterization.

##############################
INPUT: object with:

        # sink_id
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

from General.Auxiliary_General.stream import Stream
from General.Auxiliary_General.schedule_hour import schedule_hour
import json

def industry(in_var):

        # INPUT  ------------------------
        sink_id = in_var.sink_id
        streams = in_var.streams

        # Defined vars
        stream_type = 'inflow'
        streams_output = []

        # COMPUTE ------------------------
        for stream in streams:
                supply_temperature = stream['supply_temperature']
                target_temperature = stream['target_temperature']
                fluid = stream['fluid']
                fluid_cp = stream['fluid_cp']
                flowrate = stream['flowrate']
                saturday_on = stream['saturday_on']
                sunday_on = stream['sunday_on']
                shutdown_periods = stream['shutdown_periods']
                daily_periods = stream['daily_periods']

                capacity = flowrate * fluid_cp * abs((supply_temperature - target_temperature))/3600  # [kW]
                schedule = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)
                info_stream = Stream(sink_id,stream_type,fluid,supply_temperature,target_temperature,flowrate,capacity,schedule)
                streams_output.append(info_stream.__dict__)

        # OUTPUT ------------------------
        output = json.dumps(streams_output, indent=2)

        return output



