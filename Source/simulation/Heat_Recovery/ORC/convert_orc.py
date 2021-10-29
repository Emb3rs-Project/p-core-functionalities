"""
##############################
INFO: Convert_Options Raw Data to ORC/RC, for maximum electrical generation.

##############################
INPUT:

##############################
OUTPUT:


"""

from KB_General.fuel_properties import fuel_properties
from KB_General.equipment_details import equipment_details
from Source.simulation.Auxiliary.design_orc import design_orc
from General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from General.Convert_Equipments.Convert_Options.add_hx import Add_HX
from General.Auxiliary_General.flowrate_to_power import flowrate_to_power

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

    # Intermediate Circuit Characteristics
    intermediate_fluid = 'oil'

    # Convert_Options Characteristics
    fuel_data = fuel_properties(country, 'electricity', consumer_type)


    # Generate Electricity Available Profile

    # Individual Stream
    for stream in streams:

        if stream['target_temperature'] > (orc_T_evap + hx_delta_T):

            if stream['supply_temperature'] > (orc_T_evap + hx_delta_T):

                orc_type, stream_thermal_capacity_max_power, orc_electrical_generation, overall_thermal_capacity, stream_target_temperature_corrected, intermediate_circuit, hx_intermediate_supply_temperature, hx_intermediate_return_temperature = design_orc(
                    stream['capacity'], stream['fluid'], stream['supply_temperature'], stream['target_temperature'],
                    hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency)

                global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details(orc_type,
                                                                                                        orc_electrical_generation)

                # INTERMEDIATE CIRCUIT
                if intermediate_circuit == True:
                    # add HX intermediate
                    hx_stream_supply_temperature = stream['supply_temperature']
                    hx_stream_target_temperature = stream_target_temperature_corrected
                    hx_power = stream_thermal_capacity_max_power
                    info_hx_intermediate = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature,
                                                  stream['fluid'], hx_intermediate_supply_temperature,
                                                  hx_intermediate_return_temperature, intermediate_fluid, hx_power,
                                                  power_fraction)

                    # add intermediation circulation pumping
                    info_pump_intermediate = Add_Pump(country, consumer_type, intermediate_fluid,
                                                      info_hx_intermediate.available_power, power_fraction,
                                                      hx_intermediate_supply_temperature,
                                                      hx_intermediate_return_temperature)

                else:
                    hx_intermediate_turnkey = 0
                    hx_intermediate_om_fix = 0
                    pumping_intermediate_turnkey = 0
                    pumping_intermediate_om_fix = 0
                    pumping_intermediate_flowrate = 0

                # TOTAL DESIGN/COST
                total_turnkey_max_power = turnkey_total + hx_intermediate_turnkey + pumping_intermediate_turnkey
                total_om_fix_max_power = om_fix_total + hx_intermediate_om_fix + pumping_intermediate_om_fix
                total_om_var_max_power = flowrate_to_power(pumping_intermediate_flowrate) * fuel_properties[
                    'price']  # [kW]*[€/kWh] = [€/h]


    # Aggregate streams
    for stream in streams:

        if stream['target_temperature'] > (orc_T_evap + hx_delta_T + pumping_delta_T):

            if stream['supply_temperature'] > (orc_T_evap + hx_delta_T):

                orc_type, stream_thermal_capacity_max_power, orc_electrical_generation, overall_thermal_capacity, stream_target_temperature_corrected, intermediate_circuit, hx_intermediate_supply_temperature, hx_intermediate_return_temperature = design_orc(
                    stream['capacity'], stream['fluid'], stream['supply_temperature'], stream['target_temperature'], hx_delta_T,orc_T_cond, orc_T_evap, hx_efficiency)

                global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details(orc_type, orc_electrical_generation)

                # INTERMEDIATE CIRCUIT
                if intermediate_circuit == True:
                    # add HX intermediate
                    hx_stream_supply_temperature = stream['supply_temperature']
                    hx_stream_target_temperature = stream_target_temperature_corrected
                    hx_power = stream_thermal_capacity_max_power
                    info_hx_intermediate = Add_HX(hx_stream_supply_temperature, hx_stream_target_temperature,
                                                  stream['fluid'], hx_intermediate_supply_temperature,
                                                  hx_intermediate_return_temperature, intermediate_fluid, hx_power,
                                                  power_fraction)

                    # add intermediation circulation pumping
                    info_pump_intermediate = Add_Pump(country, consumer_type, intermediate_fluid,
                                                      info_hx_intermediate.available_power, power_fraction,
                                                      hx_intermediate_supply_temperature,
                                                      hx_intermediate_return_temperature)

                else:
                    hx_intermediate_turnkey = 0
                    hx_intermediate_om_fix = 0
                    pumping_intermediate_turnkey = 0
                    pumping_intermediate_om_fix = 0
                    pumping_intermediate_flowrate = 0

                # TOTAL DESIGN/COST
                total_turnkey_max_power = turnkey_total + hx_intermediate_turnkey + pumping_intermediate_turnkey
                total_om_fix_max_power = om_fix_total + hx_intermediate_om_fix + pumping_intermediate_om_fix
                total_om_var_max_power = flowrate_to_power(pumping_intermediate_flowrate) * fuel_properties['price']  # [kW]*[€/kWh] = [€/h]





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


