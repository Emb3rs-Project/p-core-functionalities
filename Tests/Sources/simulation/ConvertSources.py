

from ....Source.simulation.Convert.convert_sources import convert_sources
from ....utilities.kb import KB
from ....utilities.kb_data import kb

###################################################
# JUMP THIS PART
stream_1 = {
    'id': 1,
    'object_type': 'stream',
    'stream_type': 'excess_heat',
    'fluid': 'flue_gas',
    'capacity': 434,
    'supply_temperature': 220,
    'target_temperature': 50,
    'hourly_generation': [434, 434, 434, 434, 434, 434, 434],
    'schedule': [1, 1, 1, 1, 1, 1, 1]

}

stream_2 = {
    'id': 2,
    'object_type': 'stream',
    'stream_type': 'excess_heat',
    'fluid': 'water',
    'capacity': 900,
    'supply_temperature': 90,
    'target_temperature': 30,
    'hourly_generation': [900, 900, 900, 900, 900, 900, 900],
    'schedule': [1, 1, 1, 1, 1, 1, 1]
}

group_of_sources = [{
    'id': 1,
    'consumer_type': 'non-household',
    'location': [41.14, -8.6],
    'streams': [stream_1, stream_2]
}]

grid_losses = []
last_iteration_data = []
###################################################


data = {}
data['platform'] = {'group_of_sources': group_of_sources}

data['cf-module'] = {
    'sink_group_grid_supply_temperature': 80,
    'sink_group_grid_return_temperature': 55,
    'last_iteration_data': last_iteration_data # first iteration not needed. Second iteration needed - CHECK convert_sources info
}

data['gis-module'] = {
    'grid_losses': grid_losses}  # first iteration not needed. Second iteration -> [[200],[150],...]. - CHECK convert_sources info


def testConvertSource():

    test = convert_sources(data, KB(kb))
    print(test)

    """
    Expected:
    {'all_sources_info': [{'source_id': 1, 'location': [41.14, -8.6], 'source_grid_supply_temperature': 80, 'source_grid_return_temperature': 55, 'streams_converted': [{'stream_id': 1, 'gis_capacity': 357.12455882352936, 'hourly_stream_capacity': [434, 434, 434, 434, 434, 434, 434], 'teo_capacity_factor': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 'max_stream_capacity': 434, 'conversion_technologies': [{'teo_equipment_name': 'source-1-1-multiple_heat_exchanger', 'output': 1, 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['hx_economizer', 'circulation_pumping', 'hx_plate', 'circulation_pumping'], 'max_capacity': 395.70588235294116, 'turnkey_a': 76.74026582455114, 'turnkey_b': 4271.63969728168, 'conversion_efficiency': 0.9024999999999999, 'om_fix': 8.753525242389538, 'om_var': 0.0006745842558701699, 'emissions': 0.0008000883034739225, 'technologies': [{'object_type': 'equipment', 'power': 395.70588235294116, 'available_power': 375.9205882352941, 'hot_stream_T_hot': 220, 'hot_stream_T_cold': 65, 'cold_stream_T_hot': 85, 'cold_stream_T_cold': 60, 'equipment_sub_type': 'hx_economizer', 'u_value': 50, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_economizer', 'fuel_type': 'none', 'max_input_capacity': 395.70588235294116, 'turnkey_a': 55.69161201657302, 'turnkey_b': 1278.586095532144, 'conversion_efficiency': 0.95, 'om_fix': 5.89227646290372, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'thermal_oil', 'supply_temperature': 85, 'return_temperature': 60, 'supply_capacity': 375.9205882352941, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 375.9205882352941, 'turnkey_a': 9.07782565518904, 'turnkey_b': 430.68218762247807, 'conversion_efficiency': 1.0, 'om_fix': 1.022349897317424, 'om_var': 0.0005302608344034686, 'emissions': 0.0006289140128971372}}, {'object_type': 'equipment', 'power': 375.9205882352941, 'available_power': 357.12455882352936, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 60, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 55, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'none', 'max_input_capacity': 375.9205882352941, 'turnkey_a': 7.984671783620635, 'turnkey_b': 2320.696078783104, 'conversion_efficiency': 0.95, 'om_fix': 1.4158039647501894, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 357.12455882352936, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 357.12455882352936, 'turnkey_a': 5.3620844776830205, 'turnkey_b': 241.67533534395875, 'conversion_efficiency': 1.0, 'om_fix': 0.6038810088881832, 'om_var': 0.00018929247998545687, 'emissions': 0.0002245096855641465}}]}, {'teo_equipment_name': 'source-1-1-orc', 'output': 1, 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['hx_economizer', 'circulation_pumping', 'orc', 'circulation_pumping'], 'max_capacity': 191.47058823529412, 'turnkey_a': 590.4072492967283, 'turnkey_b': 10775.840663351599, 'conversion_efficiency': 0.8111609855445302, 'electrical_conversion_efficiency': 0.05390175180693376, 'om_fix': 13.983975704028095, 'om_var': 0.000269812657863674, 'emissions': 0.0003200103616522645, 'technologies': [{'object_type': 'equipment', 'power': 191.47058823529412, 'available_power': 181.8970588235294, 'hot_stream_T_hot': 220, 'hot_stream_T_cold': 145, 'cold_stream_T_hot': 170, 'cold_stream_T_cold': 140, 'equipment_sub_type': 'hx_economizer', 'u_value': 50, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_economizer', 'fuel_type': 'none', 'max_input_capacity': 191.47058823529412, 'turnkey_a': 66.20925993526888, 'turnkey_b': 735.5098395814639, 'conversion_efficiency': 0.95, 'om_fix': 7.0050632369334895, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 170, 'return_temperature': 140, 'supply_capacity': 181.8970588235294, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 181.8970588235294, 'turnkey_a': 6.306003371895722, 'turnkey_b': 144.76342064732512, 'conversion_efficiency': 1.0, 'om_fix': 0.710185692545851, 'om_var': 0.00014241539974685222, 'emissions': 0.000168911288071848}}, {'object_type': 'equipment', 'fuel_type': 'electricity', 'equipment_sub_type': 'orc', 'supply_temperature': 85, 'overall_thermal_capacity': 172.80220588235292, 'electrical_generation': 9.314341613161256, 'supply_capacity': 155.3134710557321, 'data_teo': {'equipment': 'orc', 'fuel_type': 'electricity', 'max_eletrical_generation': 9.314341613161256, 'max_input_capacity': 172.80220588235292, 'turnkey_a': 567.5733857071463, 'turnkey_b': 9751.248555683924, 'conversion_efficiency': 0.898793335783413, 'electrical_conversion_efficiency': 0.05390175180693376, 'om_fix': 6.240035018963041, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 155.3134710557321, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 155.3134710557321, 'turnkey_a': 7.362663717671053, 'turnkey_b': 144.31884743888008, 'conversion_efficiency': 1.0, 'om_fix': 0.8291873827121851, 'om_var': 0.00016583394726986633, 'emissions': 0.00019668677466891122}}]}]}, {'stream_id': 2, 'gis_capacity': 427.5, 'hourly_stream_capacity': [900, 900, 900, 900, 900, 900, 900], 'teo_capacity_factor': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 'max_stream_capacity': 900, 'conversion_technologies': [{'teo_equipment_name': 'source-1-2-single_heat_exchanger', 'output': 1, 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['hx_plate', 'circulation_pumping'], 'max_capacity': 450.0, 'turnkey_a': 10.947133701567349, 'turnkey_b': 2513.008939187047, 'conversion_efficiency': 0.95, 'om_fix': 1.6531598010871897, 'om_var': 0.0001850417225850868, 'emissions': 0.0002194680895776611, 'technologies': [{'object_type': 'equipment', 'power': 450.0, 'available_power': 427.5, 'hot_stream_T_hot': 90, 'hot_stream_T_cold': 60, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 55, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 7.213475204444817, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'none', 'max_input_capacity': 450.0, 'turnkey_a': 6.1903814634831225, 'turnkey_b': 2242.860784012249, 'conversion_efficiency': 0.95, 'om_fix': 1.11745165390659, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 427.5, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 427.5, 'turnkey_a': 5.007107619036027, 'turnkey_b': 270.1481551747979, 'conversion_efficiency': 1.0, 'om_fix': 0.5639033128216842, 'om_var': 0.00019478076061588086, 'emissions': 0.0002310190416606959}}]}]}]}], 'teo_string': 'dhn', 'n_supply_list': [{'id': 1, 'stream_id': 1, 'coords': [41.14, -8.6], 'cap': 357.12455882352936}, {'id': 1, 'stream_id': 2, 'coords': [41.14, -8.6], 'cap': 427.5}]}
    """





