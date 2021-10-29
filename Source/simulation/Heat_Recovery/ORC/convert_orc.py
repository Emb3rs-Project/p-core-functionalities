"""
##############################
INFO: Convert_Options Raw Data to ORC/RC, for maximum electrical generation.

##############################
INPUT:

##############################
OUTPUT:


"""

from KB_General.fuel_properties import fuel_properties
from Source.simulation.Heat_Recovery.ORC.Auxiliary.convert_aux import convert_aux
import itertools


def convert_orc(in_var):

    # INPUT
    streams = in_var.streams
    consumer_type = in_var.consumer_type
    country = in_var.country

    # Initialize Arrays
    output = []

    # Defined vars
    hx_delta_T = 5
    hx_efficiency = 0.95
    power_fraction = 0.05

    pumping_delta_T = 30  # [ºC]

    # ORC Characteristics
    orc_T_evap = 110  # [ºC]
    orc_T_cond = 30   # [ºC]
    hx_orc_supply_temperature = orc_T_evap + hx_delta_T
    hx_orc_return_temperature = hx_orc_supply_temperature - pumping_delta_T

    # Intermediate Circuit Characteristics
    intermediate_fluid = 'water'

    # Convert_Options Characteristics
    fuel_data = fuel_properties(country, 'electricity', consumer_type)


    # Generate Electricity Available Profile
    streams_able = []
    for stream in streams:
        if stream['target_temperature'] > (hx_orc_return_temperature):
            if stream['supply_temperature'] > (hx_orc_supply_temperature):
                streams_able.append(stream)


    combinations =[]
    for L in range(0, len(streams_able) + 1):
        for subset in itertools.combinations(streams_able, L):
            if list(subset) != []:
                combinations.append(list(subset))

    # Test all combinations possible
    for combination in combinations:
        electrical_generation_yearly = 0
        electrical_generation_nominal = 0
        total_turnkey = 0
        electrical_generation_over_turnkey = 0

        for stream in combination:
            if stream['target_temperature'] > (hx_orc_return_temperature):
                if stream['supply_temperature'] > (hx_orc_supply_temperature):

                    # Individual Stream
                    if len(combination) == 1:
                        orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction,intermediate_fluid, country, consumer_type,aggregate_streams=False)

                    # Aggregate streams
                    else:
                        orc_electrical_generation, intermediate_turnkey_max_power, intermediate_om_fix_max_power, intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction,intermediate_fluid, country, consumer_type, aggregate_streams=True)

                electrical_generation_nominal += electrical_generation_nominal
                electrical_generation_yearly += electrical_generation_yearly
                total_turnkey += total_turnkey
                electrical_generation_over_turnkey += electrical_generation_over_turnkey

        global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type,electrical_generation)

    # OUTPUT (INFO MAX POWER)
    output = {
        'electrical_generation':orc_electrical_generation,  # [kW]
        'excess_heat_supply_capacity':stream_thermal_capacity_max_power,  # [kW]
        'conversion_efficiency':orc_electrical_generation / stream_thermal_capacity_max_power,  # [%]
        'turnkey':total_turnkey_max_power,  # [€]
        'om_fix':total_om_fix_max_power,  # [€/year]
        'om_var':total_om_var_max_power  # [€/h]
        }


    return output


