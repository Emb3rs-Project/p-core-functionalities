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
         #          'fluid_cp' [kJ/kg.K] ** OPTIONAL - introduce capacity or fluid_cp and flowrate
         #          'flowrate' [kg/h]  ** OPTIONAL - introduce capacity or fluid_cp and flowrate
         #          'capacity' [kW] ** OPTIONAL - introduce capacity or fluid_cp and flowrate
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
        #           'object_linked_id' - # Null
        #           'fluid' - water
        #           'stream_type' - inflow
        #           'schedule' - array with 1=working and 0 =not_working
        #           'hourly_generation' - array [kWh]
        #           'monthly_generation' - array [kWh]
        #           'capacity' [kW]
        #           'supply_temperature' [ºC]
        #           'target_temperature' [ºC]
        #           }

"""

from ...General.Auxiliary_General.stream_industry import stream_industry
from ...General.Auxiliary_General.schedule_hour import schedule_hour
from ...Error_Handling.error_simple_user import PlatformSimpleUser

def simple_user(in_var):
    ##########################################################################################
    # INPUT
    platform_data = PlatformSimpleUser(**in_var['platform'])

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

        # check if capacity or flowrate given
        if stream['capacity'] == None:
            try:
                capacity = (stream["flowrate"] * stream["fluid_cp"] * abs((stream["supply_temperature"] - stream["target_temperature"]))/ 3600)
                flowrate = stream['flowrate']
            except:
                pass
        else:
            capacity = stream["capacity"]
            if stream['fluid'] == "steam":
                flowrate = None
            else:
                try:
                    flowrate = stream['flowrate']
                except:
                    flowrate = capacity * 3600 /(abs(stream["supply_temperature"] - stream["target_temperature"]))


        if stream['hourly_generation'] is None:
            schedule = schedule_hour(
                stream["saturday_on"],
                stream["sunday_on"],
                stream["shutdown_periods"],
                stream["daily_periods"],
            )
            hourly_generation = None
        else:
            hourly_generation = stream['hourly_generation']
            schedule = None
            capacity = max(hourly_generation)
            flowrate = capacity * 3600 / (abs(stream["supply_temperature"] - stream["target_temperature"]))

        info_stream = stream_industry(
            None,
            stream_type,
            stream["fluid"],
            stream["supply_temperature"],
            stream["target_temperature"],
            flowrate,
            capacity,
            schedule=schedule,
            hourly_generation=hourly_generation
        )

        streams_output.append(info_stream)

    output = {'streams': streams_output}

    return output
