"""
##############################
INFO: 'Template' to create isolated streams - meant for Pinch Analysis.


##############################
INPUT: object with:
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


def isolated_stream(streams):

    ##########################################################################################
    # COMPUTE
    streams_output = []

    for stream in streams:
        if stream['capacity'] == None:
            capacity = ( stream["flowrate"] * stream["fluid_cp"] * abs((stream["supply_temperature"] - stream["target_temperature"]))/ 3600)
            flowrate = stream['flowrate']

        else:
            capacity = stream["capacity"]
            if stream['fluid'] == "steam":
                flowrate = None
            else:
                flowrate = stream['flowrate']

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

        if stream['target_temperature'] > stream["supply_temperature"]:
            stream_type = 'hot_stream'
        else:
            stream_type = 'cold_stream'


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

        info_stream['id'] = stream['id']
        info_stream['fuel'] = stream['fuel_associated']
        info_stream['eff_equipment'] = stream['eff_equipment_associated']

    output = {'streams': streams_output}

    return output
