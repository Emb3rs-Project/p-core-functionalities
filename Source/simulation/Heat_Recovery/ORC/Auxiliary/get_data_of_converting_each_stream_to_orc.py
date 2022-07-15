from ......Source.simulation.Auxiliary.design_orc import design_orc
from ......General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ......General.Convert_Equipments.Convert_Options.add_hx import Add_HX


def get_data_of_converting_each_stream_to_orc(kb, stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency,
                                              power_fraction, intermediate_fluid, fuels_data, aggregate_streams):

    """
    Auxiliary function with the purpose of designing the ORC according to the stream given, whether it is aggreagated or not,
    and make techno-economical estimates.

    :param kb: Knowledge Base Data
    :param stream: ``dict``: stream data
    :param hx_delta_T: ``float``: minimum heat exchanger temperature difference [ºC]
    :param orc_T_cond: ``float``: [OPTIONAL] ORC evaporator temperature [ºC]; DEFAULT=35
    :param orc_T_evap: ``float``: [OPTIONAL] ORC evaporator temperature [ºC]
    :param hx_efficiency: ``float``: heat exchangers efficiency []
    :param power_fraction: ``float``: value to design solution to 2 different capacities and linearize CAPEX (y=ax+b) []
    :param intermediate_fluid: ``str``: intermediate circuit fluid name []
    :param country: ``str``: country name []
    :param consumer_type: `str``: type of consumer tariff []; 'household' or 'non-household'
    :param aggregate_streams: ``boolean``: if True, it will check the available power of the stream for the intermediate circuit designed

    :return:
            - stream_thermal_capacity_max_power: ``float``: [kW]
            - orc_type: ``str``:  DEFAULT="orc"
            - orc_electrical_generation: ``float``: ORC nominal electrical generation [kW]
            - intermediate_turnkey_max_power: ``float``: turnkey for intermediate circuit (maximum stream capacity) [€]
            - intermediate_om_fix_max_power: ``float``: OM fix for intermediate circuit (maximum stream capacity) [€/year]
            - intermediate_om_var_max_power: ``float``: OM var for intermediate circuit (maximum stream capacity) [€/year]

    """

    # design orc
    orc_type, stream_thermal_capacity_max_power, orc_electrical_generation, overall_thermal_capacity, stream_target_temperature_corrected, intermediate_circuit, hx_intermediate_supply_temperature, hx_intermediate_return_temperature = design_orc(
        stream['capacity'], stream['fluid'], stream['supply_temperature'], stream['target_temperature'],
        hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, aggregate_streams)

    if orc_electrical_generation != 0:
        # design intermediate circuit
        if intermediate_circuit == True:
            # add HX intermediate
            hx_stream_supply_temperature = stream['supply_temperature']
            hx_stream_target_temperature = stream_target_temperature_corrected
            hx_power = stream_thermal_capacity_max_power
            info_hx_intermediate = Add_HX(kb,
                                          hx_stream_supply_temperature,
                                          hx_stream_target_temperature,
                                          stream['fluid'],
                                          hx_intermediate_supply_temperature,
                                          hx_intermediate_return_temperature,
                                          intermediate_fluid, hx_power,
                                          power_fraction)

            # add intermediation circulation pumping
            info_pump_intermediate = Add_Pump(kb,
                                              fuels_data,
                                              intermediate_fluid,
                                              info_hx_intermediate.available_power,
                                              power_fraction,
                                              hx_intermediate_supply_temperature,
                                              hx_intermediate_return_temperature)

            hx_intermediate_turnkey = info_hx_intermediate.data_teo['max_input_capacity'] * \
                                      info_hx_intermediate.data_teo['turnkey_a'] + info_hx_intermediate.data_teo['turnkey_b']
            hx_intermediate_om_fix = info_hx_intermediate.data_teo['max_input_capacity'] * \
                                     info_hx_intermediate.data_teo[
                                         'om_fix']
            pumping_intermediate_turnkey = info_pump_intermediate.data_teo['max_input_capacity'] * \
                                           info_pump_intermediate.data_teo['turnkey_a'] + \
                                           info_pump_intermediate.data_teo[
                                               'turnkey_b']
            pumping_intermediate_om_fix = info_pump_intermediate.data_teo['max_input_capacity'] * \
                                          info_pump_intermediate.data_teo['om_fix']
            pumping_intermediate_om_var = info_pump_intermediate.data_teo['om_var'] * info_pump_intermediate.data_teo[
                'max_input_capacity']

    # cost intermediate circuit
    try:
        intermediate_turnkey_max_power = hx_intermediate_turnkey + pumping_intermediate_turnkey  # [€]
        intermediate_om_fix_max_power = hx_intermediate_om_fix + pumping_intermediate_om_fix  # [€/year]
        intermediate_om_var_max_power = pumping_intermediate_om_var * sum(stream['schedule'])  # [€]
    except:
        intermediate_turnkey_max_power = 0
        intermediate_om_fix_max_power = 0
        intermediate_om_var_max_power = 0

    return stream_thermal_capacity_max_power, orc_type, orc_electrical_generation, intermediate_turnkey_max_power, \
           intermediate_om_fix_max_power, intermediate_om_var_max_power
