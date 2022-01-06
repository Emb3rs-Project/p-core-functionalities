"""
alisboa/jmcunha


##############################
INFO: Design ORC/RC according to the excess heat streams given.
      The following assumptions are implemetend:
       - above design_temperature = 500ºC, 'rc', below 'orc'[ºC]
       - 120 ºC is the minimum temperature flue_gas can be cooled. Design constraint - lower flue_gas temperatures mean
       condensation
       - orc_delta_T = 30

       The conversion design can be for a unique stream  or the aggregated of multiple streams. If the excess streams are
       to be aggregated to enhance the power available to convert in the ORC, a intermediate circuit characteristics are
       designed.


##############################
INPUT:
        # stream_capacity  [kW]
        # stream_fluid - fluid name
        # stream_supply_temperature  [ºC]
        # stream_target_temperature  [ºC]
        # hx_delta_T  [ºC]
        # orc_T_cond  [ºC]
        # orc_T_evap  [ºC]
        # hx_efficiency  []
        # aggregate_streams - True or False


##############################
OUTPUT:
        # orc_type - e.g. 'rc' or 'orc'
        # stream_thermal_capacity_max_power   [kW]
        # orc_electrical_generation  [kW]
        # overall_thermal_capacity - thermal+electrical [kW]
        # stream_target_temperature_corrected  [ºC]
        # intermediate_circuit_exist - True or False
        # intermediate_T_hot  [ºC]
        # intermediate_T_cold  [ºC]


"""


def design_orc(stream_capacity, stream_fluid, stream_supply_temperature, stream_target_temperature, hx_delta_T, orc_T_cond,
               orc_T_evap, hx_efficiency, aggregate_streams):

    # Defined vars
    orc_delta_T = 30  # [ºC]
    flue_gas_T_minimum = 120  # minimum temperature flue_gas can be cooled [ºC]
    design_temperature = 500  # above this temperature 'rc', below 'orc'[ºC]

    # if streams are aggregated, an intermediate circuit is implemented
    if aggregate_streams == True:
        intermediate_circuit_exist = True
        intermediate_T_hot = orc_T_evap + hx_delta_T
        intermediate_T_cold = intermediate_T_hot - orc_delta_T
        orc_type = 'orc'

        if stream_fluid == 'flue_gas':
            stream_target_temperature_corrected_min = flue_gas_T_minimum  # design constraint - lower flue_gas temperatures mean condensation
        else:
            stream_target_temperature_corrected_min = intermediate_T_cold + hx_delta_T

        stream_target_temperature_corrected = intermediate_T_cold + hx_delta_T

    if aggregate_streams == False:
        if stream_supply_temperature < design_temperature:
            orc_type = 'orc'
            intermediate_T_cold = orc_T_evap + hx_delta_T
            if stream_fluid == 'flue_gas':
                stream_target_temperature_corrected_min = flue_gas_T_minimum  # design constraint - lower flue_gas temperatures mean condensation
            else:
                stream_target_temperature_corrected_min = orc_T_evap + hx_delta_T

            stream_target_temperature_corrected = orc_T_evap + 2 * hx_delta_T

            # from the suppliers info gathered, it was seen that water streams could be directly fed to the orc system,
            # otherwise an intermediate circuit was needed
            if stream_fluid != 'water':
                intermediate_circuit_exist = True
            else:
                intermediate_circuit_exist = False

        else:
            orc_type = 'rc'
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
    stream_thermal_capacity_max_power = stream_capacity * (stream_supply_temperature - stream_target_temperature_corrected) \
                                        / (stream_supply_temperature - stream_target_temperature)
    eff_carnot = 1 - (orc_T_cond + 273.15) / (orc_T_evap + 273.15)

    if intermediate_circuit_exist == True:
        overall_thermal_capacity = stream_thermal_capacity_max_power * hx_efficiency ** 2
    else:
        overall_thermal_capacity = stream_thermal_capacity_max_power * hx_efficiency

    orc_electrical_generation = overall_thermal_capacity * eff_carnot


    return orc_type, stream_thermal_capacity_max_power, orc_electrical_generation, overall_thermal_capacity, \
           stream_target_temperature_corrected, intermediate_circuit_exist, intermediate_T_hot, intermediate_T_cold
