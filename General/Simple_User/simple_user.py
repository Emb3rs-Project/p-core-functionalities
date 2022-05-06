"""
##############################
INFO: Simple User streams characterization. Receives user's streams data from the platform and creates a standard
      stream data output to be used in other modules.

##############################
INPUT: object with:

        # id
        # type_of_object - 'sink' or 'source'
        # streams - array with dictionaries

        Where in streams:
         # streams = {
         #          'supply_temperature' [ºC]
         #          'target_temperature' [ºC]
         #          'fluid - name
         #          'fluid_cp' [kJ/kg.K]
         #          'flowrate' [kg/h]
         #          'saturday_on' - 1 (yes)  or 0 (no)
         #          'sunday_on' - 1 (yes)  or 0 (no)
         #          'shutdown_periods' - array with day arrays e.g. [[130,140],[289,299]]
         #          'daily_periods' - array with hour arrays; e.g. [[8,12],[15,19]]
         #          }

##############################
OUTPUT: dict with key 'streams' with streams dictionaries, e.g. 'streams' =[stream_1,stream_2, ... :

        Where for example:
        # stream_1 = {
        #           'id' - stream id
        #           'object_type' - stream
        #           'object_id' - # Object ID associated; e.g. process or equipment ID
        #           'fluid' - water
        #           'stream_type' - inflow
        #           'schedule' - array with 1=working and 0 =not_working
        #           'hourly_generation' - array [kWh]
        #           'capacity' [kW]
        #           'supply_temperature' [ºC]
        #           'target_temperature' [ºC]
        #           }

"""

from ...General.Auxiliary_General.stream_industry import stream_industry
from ...General.Auxiliary_General.schedule_hour import schedule_hour
from ...Error_Handling.error_simple_industry import PlatformSimpleIndustry

def simple_user(in_var):


    ##########################################################################################
    # INPUT
    platform_data = PlatformSimpleIndustry(**in_var['platform'])

    object_id = platform_data.object_id
    streams = platform_data.streams
    streams = [vars(stream) for stream in streams]
    type_of_object = platform_data.type_of_object

    ##########################################################################################
    # COMPUTE
    streams_output = []

    if type_of_object == 'sink':
        stream_type = "inflow"
    else:
        stream_type = "excess_heat"

    for stream in streams:

        capacity = (
                stream["flowrate"]
                * stream["fluid_cp"]
                * abs((stream["supply_temperature"] - stream["target_temperature"]))
                / 3600
        )  # [kW]



        if stream['hourly_generation'] is None:
            schedule = schedule_hour(
                stream["saturday_on"],
                stream["sunday_on"],
                stream["shutdown_periods"],
                stream["daily_periods"],
            )
            hourly_generation = None
        else:
            schedule = None
            hourly_generation = stream['hourly_generation']

        info_stream = stream_industry(
            object_id,
            stream_type,
            stream["fluid"],
            stream["supply_temperature"],
            stream["target_temperature"],
            stream["flowrate"],
            capacity,
            schedule=schedule,
            hourly_generation=hourly_generation
        )

        streams_output.append(info_stream)

    output = {'streams': streams_output}

    return output
