def design_orc(stream_capacity, stream_fluid, stream_supply_temperature, stream_target_temperature, hx_delta_T, orc_T_cond,
               orc_T_evap, hx_efficiency, aggregate_streams):
    """Design ORC according to the excess heat streams given.

    The following assumptions are implemented:
        - 120 ºC is the minimum temperature flue_gas can be cooled. Design constraint - lower flue_gas temperatures mean
     condensation;
        - orc_delta_T = 30;
     The conversion design can be for a unique stream  or the aggregated of multiple streams. If the excess streams are
     to be aggregated to enhance the power available to convert in the ORC, a intermediate circuit is designed.


    Parameters
    ----------
    stream_capacity : float
        given stream capacity (it may be corrected) [kW]

    stream_fluid : str
        stream fluid []

    stream_supply_temperature : float
        stream supply/initial temperature [ºC]

    stream_target_temperature : float
        given stream target/final temeprature (it may be corrected) [ºC]

    hx_delta_T : float
        minimum heat exchangers temperature difference [ºC]

    orc_T_cond : float
        ORC condenser temperature [ºC]

    orc_T_evap : float
        ORC evaporator temperature [ºC]

    hx_efficiency : float
        heat exchanger efficiency []

    aggregate_streams : boolean
        design ORC for the aggregate of multiple streams or not


    Returns
    -------
    orc_type : str
        DEFAULT="orc"

    stream_thermal_capacity_max_power : float
        Maximum convertible stream capacity [kW]

    orc_electrical_generation : float
        ORC nominal electrical generation [kW]

    overall_thermal_capacity : float
        Thermal conversion efficiency []

    stream_target_temperature_corrected : float
        Stream target/final temeprature (it may be corrected) [ºC]

    intermediate_circuit_exist : boolean
        Whether intermediate circuit should be designed

    intermediate_T_hot : float
        Intermediate circuit fluid' highest temperature [ºC]

    intermediate_T_cold : float
        Intermediate circuit fluid' lowest temperature [ºC]

    """

    ################################################
    # Defined vars
    orc_type = 'orc'
    carnot_correction_factor = 0.44
    orc_delta_T = 30  # [ºC]
    flue_gas_T_minimum = 120  # minimum temperature flue_gas can be cooled [ºC]


    ################################################
    intermediate_T_cold = orc_T_evap + hx_delta_T

    # if streams are aggregated, an intermediate circuit is implemented
    if aggregate_streams == True:
        intermediate_circuit_exist = True
        number_hx = 2
        if stream_fluid == 'flue_gas' or stream_fluid == 'flue_gas':
            stream_target_temperature_corrected_min = flue_gas_T_minimum
        else:
            stream_target_temperature_corrected_min = intermediate_T_cold + hx_delta_T

        stream_target_temperature_corrected = orc_T_evap + hx_delta_T * number_hx

    else:
        if stream_fluid == 'flue gas' or stream_fluid == 'flue_gas':
            stream_target_temperature_corrected_min = flue_gas_T_minimum  # design constraint - lower flue_gas temperatures mean condensation
        else:
            stream_target_temperature_corrected_min = orc_T_evap + hx_delta_T

        # from the suppliers - water streams can be directly fed to the orc system, otherwise implement intermediate circuit
        if stream_fluid != 'water':
            intermediate_circuit_exist = True
            number_hx = 2
        else:
            intermediate_circuit_exist = False
            number_hx = 1

        stream_target_temperature_corrected = orc_T_evap + number_hx * hx_delta_T

    if stream_target_temperature_corrected <= stream_target_temperature_corrected_min:
        stream_target_temperature_corrected = stream_target_temperature_corrected_min

    if stream_target_temperature_corrected <= stream_target_temperature:
        stream_target_temperature_corrected = stream_target_temperature

    intermediate_T_hot = intermediate_T_cold + orc_delta_T
    if intermediate_T_hot > stream_supply_temperature - hx_delta_T:
        intermediate_T_hot = stream_supply_temperature - hx_delta_T

    if stream_supply_temperature > stream_target_temperature_corrected:
        stream_thermal_capacity_max_power = stream_capacity * (stream_supply_temperature - stream_target_temperature_corrected) / (stream_supply_temperature - stream_target_temperature)

        # get eff. carnot
        eff_carnot = (1 - (orc_T_cond + 273.15) / (orc_T_evap + 273.15)) * carnot_correction_factor

        # get overall thermal capacity
        overall_thermal_capacity = stream_thermal_capacity_max_power * hx_efficiency ** number_hx

        # get electrical generation
        orc_electrical_generation = overall_thermal_capacity * eff_carnot

    else:
        stream_thermal_capacity_max_power = 0
        orc_electrical_generation = 0
        overall_thermal_capacity = 0

    return orc_type, stream_thermal_capacity_max_power, orc_electrical_generation, overall_thermal_capacity, \
           stream_target_temperature_corrected, intermediate_circuit_exist, intermediate_T_hot, intermediate_T_cold
