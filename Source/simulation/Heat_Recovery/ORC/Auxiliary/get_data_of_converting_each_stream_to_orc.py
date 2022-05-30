"""
alisboa/jmcunha


##############################
INFO: Auxiliary function to the main script, with the purpose of designing the orc according to the stream given and
      estimate costs.


##############################
INPUT:
        # stream - stream dictionary with its characteristics, e.g. capacity, fluid, supply_temperature, target_temperature
        # hx_delta_T  [ºC]
        # orc_T_cond  [ºC]
        # orc_T_evap  [ºC]
        # hx_efficiency  []
        # power_fraction  []
        # intermediate_fluid - fluid name
        # country - country name
        # consumer_type - e.g. 'household' or 'non_household'
        # aggregate_streams - if True, it will check the available power of the stream for the intermediate circuit designed;
         True or False


##############################
OUTPUT:
        # stream_thermal_capacity_max_power  [kW]
        # orc_type - e.g. 'rc' or 'orc'
        # orc_electrical_generation  [kW]
        # intermediate_turnkey_max_power  [€]
        # intermediate_om_fix_max_power  [€/year]
        # intermediate_om_var_max_power  [€/year]


"""

from ......Source.simulation.Auxiliary.design_orc import design_orc
from ......General.Convert_Equipments.Convert_Options.add_pump import Add_Pump
from ......General.Convert_Equipments.Convert_Options.add_hx import Add_HX


def get_data_of_converting_each_stream_to_orc(kb,stream, hx_delta_T, orc_T_cond, orc_T_evap, hx_efficiency, power_fraction, intermediate_fluid, country,
                consumer_type, aggregate_streams):

    # design orc/rc
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
            info_hx_intermediate = Add_HX(kb, hx_stream_supply_temperature, hx_stream_target_temperature, stream['fluid'],
                                          hx_intermediate_supply_temperature, hx_intermediate_return_temperature,
                                          intermediate_fluid, hx_power, power_fraction)

            # add intermediation circulation pumping
            info_pump_intermediate = Add_Pump(kb, country, consumer_type, intermediate_fluid,
                                              info_hx_intermediate.available_power, power_fraction,
                                              hx_intermediate_supply_temperature, hx_intermediate_return_temperature)

            hx_intermediate_turnkey = info_hx_intermediate.data_teo['max_input_capacity'] * info_hx_intermediate.data_teo[
                'turnkey_a'] + info_hx_intermediate.data_teo['turnkey_b']
            hx_intermediate_om_fix = info_hx_intermediate.data_teo['max_input_capacity'] * info_hx_intermediate.data_teo[
                'om_fix']
            pumping_intermediate_turnkey = info_pump_intermediate.data_teo['max_input_capacity'] * \
                                           info_pump_intermediate.data_teo['turnkey_a'] + info_pump_intermediate.data_teo[
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

    return stream_thermal_capacity_max_power, orc_type, orc_electrical_generation, intermediate_turnkey_max_power,\
               intermediate_om_fix_max_power, intermediate_om_var_max_power
