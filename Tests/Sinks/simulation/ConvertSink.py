

from ....Sink.simulation.Convert.convert_sinks import convert_sinks


class ConvertSink():
    def __init__(self):

        stream_1 = {
            'id':2,
            'object_type':'stream',
            'stream_type':'inflow',
            'fluid':'water',
            'capacity':263,
            'supply_temperature':10,
            'target_temperature':80,
            'hourly_generation':[1000, 1000, 1000]}

        self.group_of_sinks = [{
                                'id':1,
                                'consumer_type':'non-household',
                                'location':[10, 10],
                                'streams':[stream_1]
                            },
                            {
                                'id':56,
                                'consumer_type':'household',
                                'location':[11, 11],
                                'streams':[stream_1]
                                }]


def testConvertSink():

    data = ConvertSink()
    test = convert_sinks(data)

    """
    print(test['sink_group_grid_supply_temperature'])
    print(test['grid_specific']['heating'])
    print(test['grid_specific']['cooling'])
    print(test['sinks'][0])
    
    Expected:
    85
    [{'equipment': 'hot_water_boiler', 'fuel_type': 'electricity', 'max_input_capacity': 531.3131313131313, 'turnkey_a': 28.441857380374763, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.99, 'om_fix': 1.9305, 'om_var': 0.0869, 'emissions': 0.25757575757575757}, {'equipment': 'hot_water_boiler', 'fuel_type': 'natural_gas', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 28.441857380374763, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 1.796997322981104, 'om_var': 0.03106451148390813, 'emissions': 0.2277973036269818}, {'equipment': 'hot_water_boiler', 'fuel_type': 'fuel_oil', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 28.441857380374763, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 1.796997322981104, 'om_var': 0.065911153, 'emissions': 0.28894354037691566}, {'equipment': 'hot_water_boiler', 'fuel_type': 'biomass', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 28.441857380374763, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 1.796997322981104, 'om_var': 0.043199654, 'emissions': 0.3971625282201407}]
    []
    {'sink_id': 1, 'streams': [{'stream_id': 2, 'hourly_stream_capacity': [1000, 1000, 1000], 'conversion_technologies': [{'equipment': ['circulation_pumping', 'hx_plate'], 'max_capacity': 1052.6315789473686, 'turnkey_a': 6.398171931459389, 'turnkey_b': 3120.113195638638, 'conversion_efficiency': 0.9499999999999998, 'om_fix': 0.001, 'om_var': 6.495984736816097e-08, 'emissions': 0.255, 'tecnhologies': [{'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 85, 'return_temperature': 15, 'supply_capacity': 1052.6315789473686, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 1052.6315789473686, 'turnkey_a': 1.866846081331216, 'turnkey_b': 248.00695967771503, 'conversion_efficiency': 1, 'om_fix': 0.0, 'om_var': 6.495984736816097e-08, 'emissions': 0.255}}, {'object_type': 'equipment', 'power': 1052.6315789473686, 'available_power': 1000.0000000000001, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 15, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 10, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'non', 'max_input_capacity': 1108.03324099723, 'turnkey_a': 4.304759557621765, 'turnkey_b': 2872.106235960923, 'conversion_efficiency': 0.95, 'om_fix': 0.0009500000000000001, 'om_var': 0.0, 'emissions': 0}}]}, {'equipment': ['circulation_pumping', 'hx_plate'], 'max_capacity': 1052.6315789473686, 'turnkey_a': 6.398171931459389, 'turnkey_b': 3120.113195638638, 'conversion_efficiency': 0.9499999999999998, 'om_fix': 0.001, 'om_var': 6.495984736816097e-08, 'emissions': 0.255, 'tecnhologies': [{'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 85, 'return_temperature': 15, 'supply_capacity': 1052.6315789473686, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 1052.6315789473686, 'turnkey_a': 1.866846081331216, 'turnkey_b': 248.00695967771503, 'conversion_efficiency': 1, 'om_fix': 0.0, 'om_var': 6.495984736816097e-08, 'emissions': 0.255}}, {'object_type': 'equipment', 'power': 1052.6315789473686, 'available_power': 1000.0000000000001, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 15, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 10, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'non', 'max_input_capacity': 1108.03324099723, 'turnkey_a': 4.304759557621765, 'turnkey_b': 2872.106235960923, 'conversion_efficiency': 0.95, 'om_fix': 0.0009500000000000001, 'om_var': 0.0, 'emissions': 0}}]}]}, {'stream_id': 2, 'hourly_stream_capacity': [1000, 1000, 1000], 'conversion_technologies': [{'equipment': ['circulation_pumping', 'hx_plate'], 'max_capacity': 1052.6315789473686, 'turnkey_a': 6.398171931459389, 'turnkey_b': 3120.113195638638, 'conversion_efficiency': 0.9499999999999998, 'om_fix': 0.001, 'om_var': 6.495984736816097e-08, 'emissions': 0.255, 'tecnhologies': [{'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 85, 'return_temperature': 15, 'supply_capacity': 1052.6315789473686, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 1052.6315789473686, 'turnkey_a': 1.866846081331216, 'turnkey_b': 248.00695967771503, 'conversion_efficiency': 1, 'om_fix': 0.0, 'om_var': 6.495984736816097e-08, 'emissions': 0.255}}, {'object_type': 'equipment', 'power': 1052.6315789473686, 'available_power': 1000.0000000000001, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 15, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 10, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'non', 'max_input_capacity': 1108.03324099723, 'turnkey_a': 4.304759557621765, 'turnkey_b': 2872.106235960923, 'conversion_efficiency': 0.95, 'om_fix': 0.0009500000000000001, 'om_var': 0.0, 'emissions': 0}}]}, {'equipment': ['circulation_pumping', 'hx_plate'], 'max_capacity': 1052.6315789473686, 'turnkey_a': 6.398171931459389, 'turnkey_b': 3120.113195638638, 'conversion_efficiency': 0.9499999999999998, 'om_fix': 0.001, 'om_var': 6.495984736816097e-08, 'emissions': 0.255, 'tecnhologies': [{'object_type': 'equipment', 'equipment_sub_type': 'circulation_pumping', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.215, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'fluid': 'water', 'supply_temperature': 85, 'return_temperature': 15, 'supply_capacity': 1052.6315789473686, 'global_conversion_efficiency': 1.0, 'data_teo': {'equipment': 'circulation_pumping', 'fuel_type': 'electricity', 'max_input_capacity': 1052.6315789473686, 'turnkey_a': 1.866846081331216, 'turnkey_b': 248.00695967771503, 'conversion_efficiency': 1, 'om_fix': 0.0, 'om_var': 6.495984736816097e-08, 'emissions': 0.255}}, {'object_type': 'equipment', 'power': 1052.6315789473686, 'available_power': 1000.0000000000001, 'hot_stream_T_hot': 85, 'hot_stream_T_cold': 15, 'cold_stream_T_hot': 80, 'cold_stream_T_cold': 10, 'equipment_sub_type': 'hx_plate', 'u_value': 2000, 'delta_T_lmtd': 5, 'global_conversion_efficiency': 0.95, 'data_teo': {'equipment': 'hx_plate', 'fuel_type': 'non', 'max_input_capacity': 1108.03324099723, 'turnkey_a': 4.304759557621765, 'turnkey_b': 2872.106235960923, 'conversion_efficiency': 0.95, 'om_fix': 0.0009500000000000001, 'om_var': 0.0, 'emissions': 0}}]}]}]}

    """


