

from ....Source.simulation.Convert.convert_sources import convert_sources


class ConvertSource():
    def __init__(self):

        self.grid_losses = []  # first iteration not needed. Second iteration -> [[200],[150],...]. - CHECK convert_sources info
        self.last_iteration_data = []  # first iteration not needed. Second iteration needed - CHECK convert_sources info
        self.sink_group_grid_supply_temperature = 80
        self.sink_group_grid_return_temperature = 55

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

        self.group_of_sources = [{'id': 1,
                                  'consumer_type': 'non-household',
                                  'location': [41.14, -8.6],
                                  'streams': [stream_1,stream_2]
                                  }]


def testConvertSource():

    data = ConvertSource()
    test = convert_sources(data)

    print(test)

    """
    print(sources['streams_converted'][0].keys())

     Expected:
    {'all_sources_info': [{'source_id': 1, 'location': [41.14, -8.6], 'source_grid_supply_temperature': 80, 'source_grid_return_temperature': 55, 'streams_converted': [{'stream_id': 1, 'gis_capacity': 357.12455882352936, 'hourly_stream_capacity': [434, 434, 434, 434, 434, 434, 434], 'teo_capacity_factor': [2.4285714285714284, 2.4285714285714284, 2.4285714285714284, 2.4285714285714284, 2.4285714285714284, 2.4285714285714284, 2.4285714285714284], 'conversion_technologies': [{'teo_equipment_name': 'multiple_heat_exchanger', 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['hx_economizer', 'circulation_pumping', 'hx_plate', 'circulation_pumping'], 'max_capacity': 395.70588235294116, 'turnkey_a': 76.74026582455114, 'turnkey_b': 4271.63969728168, 'conversion_efficiency': 0.9024999999999999, 'om_fix': 8.753525242389538, 'om_var': 0.0006745842558701699, 'emissions': 0.0008000883034739225, 'technologies': [{'object_type': 'equipment', 'power': 395.70588235294116, 'available_power': 375.9205882352941, 'hot_stream_T_hot': 220, 'hot_stream_T_cold': 65, 'cold_stream_T_hot': 85, 'cold_stream_T_cold': 60, 'equipment_sub_type': 'hx_economizer', 'u_value': 50, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_economizer', 'fuel_type': 'none', 'max_input_capacity': 395.70588235294116, 'turnkey_a': 55.69161201657302, 'turnkey_b': 1278.586095532144, 'conversion_efficiency': 0.95, 'om_fix': 5.89227646290372, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'thermal_oil', 'supply_temperature': 85, 'return_temperature': 60, 'supply_capacity': 375.9205882352941, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 375.9205882352941, 'turnkey_a': 9.07782565518904, 'turnkey_b': 430.68218762247807, 'conversion_efficiency': 1.0, 'om_fix': 1.022349897317424, 'om_var': 0.0005302608344034686, 'emissions': 0.0006289140128971372}}, {'object_type': 'equipment', 'power': 375.9205882352941, 'available_power': 357.12455882352936, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 60, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 55, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'none', 'max_input_capacity': 375.9205882352941, 'turnkey_a': 7.984671783620635, 'turnkey_b': 2320.696078783104, 'conversion_efficiency': 0.95, 'om_fix': 1.4158039647501894, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 357.12455882352936, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 357.12455882352936, 'turnkey_a': 5.3620844776830205, 'turnkey_b': 241.67533534395875, 'conversion_efficiency': 1.0, 'om_fix': 0.6038810088881832, 'om_var': 0.00018929247998545687, 'emissions': 0.0002245096855641465}}]}, {'teo_equipment_name': 'orc', 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['orc', 'circulation_pumping'], 'max_capacity': 178.7058823529412, 'turnkey_a': 904.2793021164713, 'turnkey_b': 16094.87413064565, 'conversion_efficiency': 0.7536142593489047, 'om_fix': 99.43427847435207, 'om_var': 0.00012217525987722047, 'emissions': 0.00014490554078461034, 'technologies': [{'object_type': 'equipment', 'fuel_type': 'electricity', 'equipment_sub_type': 'orc', 'supply_temperature': 90, 'overall_thermal_capacity': 161.2820588235294, 'electrical_generation': 19.518583906998607, 'supply_capacity': 134.67530117070427, 'data_teo': {'equipment': 'orc', 'fuel_type': 'electricity', 'max_eletrical_generation': 19.518583906998607, 'max_input_capacity': 161.2820588235294, 'turnkey_a': 995.4804536383962, 'turnkey_b': 15962.750206738681, 'conversion_efficiency': 0.835029650248094, 'electrical_conversion_efficiency': 0.12102142079148015, 'om_fix': 109.44545758884396, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 134.67530117070427, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 134.67530117070427, 'turnkey_a': 7.773463194393632, 'turnkey_b': 132.12392390695436, 'conversion_efficiency': 1.0, 'om_fix': 0.8754518538309174, 'om_var': 0.0001621190925749938, 'emissions': 0.00019228078421685313}}]}]}, {'stream_id': 2, 'gis_capacity': 427.5, 'hourly_stream_capacity': [900, 900, 900, 900, 900, 900, 900], 'teo_capacity_factor': [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], 'conversion_technologies': [{'teo_equipment_name': 'single_heat_exchanger', 'input_fuel': 'excess_heat', 'output_fuel': 'dhn_water_source', 'equipment': ['hx_plate', 'circulation_pumping'], 'max_capacity': 450.0, 'turnkey_a': 10.947133701567349, 'turnkey_b': 2513.008939187047, 'conversion_efficiency': 0.95, 'om_fix': 1.6531598010871897, 'om_var': 0.0001850417225850868, 'emissions': 0.0002194680895776611, 'technologies': [{'object_type': 'equipment', 'power': 450.0, 'available_power': 427.5, 'hot_stream_T_hot': 90, 'hot_stream_T_cold': 60, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 55, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 7.213475204444817, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'none', 'max_input_capacity': 450.0, 'turnkey_a': 6.1903814634831225, 'turnkey_b': 2242.860784012249, 'conversion_efficiency': 0.95, 'om_fix': 1.11745165390659, 'om_var': 0.0, 'emissions': 0}}, {'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 80, 'return_temperature': 55, 'supply_capacity': 427.5, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 427.5, 'turnkey_a': 5.007107619036027, 'turnkey_b': 270.1481551747979, 'conversion_efficiency': 1.0, 'om_fix': 0.5639033128216842, 'om_var': 0.00019478076061588086, 'emissions': 0.0002310190416606959}}]}]}]}], 'n_supply_list': [{'id': 1, 'stream_id': 1, 'coords': [41.14, -8.6], 'cap': 357.12455882352936}, {'id': 1, 'stream_id': 2, 'coords': [41.14, -8.6], 'cap': 427.5}]}
     """





