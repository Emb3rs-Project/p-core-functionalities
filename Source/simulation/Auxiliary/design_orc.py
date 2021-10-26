"""
@author: jmcunha/alisboa

Info: Design ORC

"""


def design_orc(stream_capacity,stream_fluid,stream_supply_temperature,stream_target_temperature,hx_delta_T,orc_T_cond,orc_T_evap, hx_efficiency):


    flue_gas_T_minimum = 120  # minimum temperature flue_gas can be cooled [ºC]
    design_temperature = 350  # above this temperature 'rc', below 'orc'[ºC]

    if stream_supply_temperature < design_temperature:
        orc_type = 'orc'
        intermediate_T_cold = orc_T_evap + hx_delta_T
        if stream_fluid == 'flue_gas':
            stream_target_temperature_corrected_min = flue_gas_T_minimum # Design Constraint - lower flue_gas temperatures mean condensation
        else:
            stream_target_temperature_corrected_min = orc_T_evap + hx_delta_T

        stream_target_temperature_corrected = orc_T_evap + 2*hx_delta_T

        intermediate_circuit_exist = True
    else:
        orc_type = 'rc' # WASTE HEAT BOILER
        intermediate_T_cold = 0  # just to run
        if stream_fluid == 'flue_gas':
            stream_target_temperature_corrected_min = flue_gas_T_minimum
        else:
            stream_target_temperature_corrected_min = orc_T_evap + hx_delta_T
        stream_target_temperature_corrected = orc_T_evap + hx_delta_T
        intermediate_circuit_exist = False

    if stream_target_temperature_corrected <= stream_target_temperature_corrected_min:
        stream_target_temperature_corrected = stream_target_temperature_corrected_min

    if stream_target_temperature_corrected < stream_target_temperature:
        stream_target_temperature_corrected = stream_target_temperature

    intermediate_T_hot = stream_supply_temperature - hx_delta_T
    stream_thermal_capacity_max_power = stream_capacity * ((stream_supply_temperature - stream_target_temperature_corrected) / (stream_supply_temperature - stream_target_temperature))
    eff_carnot = 1 - (orc_T_cond + 274.15) / (orc_T_evap + 274.15)

    if intermediate_circuit_exist == True:
        overall_thermal_capacity = stream_thermal_capacity_max_power * hx_efficiency**2
    else:
        overall_thermal_capacity = stream_thermal_capacity_max_power * hx_efficiency

    orc_electrical_generation = overall_thermal_capacity * eff_carnot

    return orc_type,stream_thermal_capacity_max_power,orc_electrical_generation,overall_thermal_capacity,stream_target_temperature_corrected,intermediate_circuit_exist, intermediate_T_hot,intermediate_T_cold