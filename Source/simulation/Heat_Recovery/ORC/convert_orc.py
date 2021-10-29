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
from KB_General.equipment_details import equipment_details


def convert_orc(in_var):

    # INPUT
    streams = in_var.streams
    consumer_type = in_var.consumer_type
    country = in_var.country

    # Initialize Arrays
    output = []
    convert_info = []

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
    combination_streams_id = []
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
        stream_thermal_capacity_total = 0

        for stream in combination:
            if stream['target_temperature'] > (hx_orc_return_temperature):
                if stream['supply_temperature'] > (hx_orc_supply_temperature):

                    # Individual Stream
                    if len(combination) == 1:
                        aggregate_streams = False
                        stream_thermal_capacity_max_power, orc_type, orc_electrical_generation,intermediate_turnkey_max_power,intermediate_om_fix_max_power,intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction,intermediate_fluid, country, consumer_type,aggregate_streams)

                    # Aggregate streams
                    else:
                        aggregate_streams = True
                        stream_thermal_capacity_max_power, orc_type, orc_electrical_generation, intermediate_turnkey_max_power, intermediate_om_fix_max_power, intermediate_om_var_max_power = convert_aux(stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction,intermediate_fluid, country, consumer_type, aggregate_streams)

                electrical_generation_nominal += electrical_generation_nominal
                electrical_generation_yearly += electrical_generation_yearly * sum(stream['schedule'])
                total_turnkey += total_turnkey
                combination_streams_id.append(stream['id'])
                stream_thermal_capacity_total += stream_thermal_capacity_max_power

        if aggregate_streams == True:
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details('orc',electrical_generation_nominal)
        else:
            global_conversion_efficiency_equipment, om_fix_orc, turnkey_orc = equipment_details(orc_type,electrical_generation_nominal)

        om_var_total = intermediate_om_var_max_power
        om_fix_total = intermediate_om_fix_max_power + om_fix_orc
        total_turnkey += turnkey_orc

        convert_info.append({
            'streams': combination_streams_id,
            'electrical_generation_nominal': electrical_generation_nominal,  # [kW]
            'electrical_generation_yearly':electrical_generation_yearly,  # [kWh]
            'excess_heat_supply_capacity': stream_thermal_capacity_total,  # [kW]
            'conversion_efficiency': orc_electrical_generation / stream_thermal_capacity_total,  # [%]
            'turnkey': total_turnkey,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€/h]
            })



    # OUTPUT (INFO MAX POWER)
    for convert in convert_info
    output = {
        'electrical_generation': orc_electrical_generation,  # [kW]
        'excess_heat_supply_capacity': stream_thermal_capacity_max_power,  # [kW]
        'conversion_efficiency': orc_electrical_generation / stream_thermal_capacity_max_power,  # [%]
        'turnkey': total_turnkey_max_power,  # [€]
        'om_fix': total_om_fix_max_power,  # [€/year]
        'om_var': total_om_var_max_power  # [€/h]
        }


    return output


