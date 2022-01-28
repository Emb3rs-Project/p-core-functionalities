

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
            'schedule': [1,1,1],
            'hourly_generation':[1000, 1000, 1000]}

        self.group_of_sinks = [{
                                'id':1,
                                'consumer_type':'non-household',
                                'location':[41.14, -8.6],
                                'streams':[stream_1]
                            },
                            {
                                'id':56,
                                'consumer_type':'household',
                                'location':[41.14, -8.6],
                                'streams':[stream_1]
                                }]


def testConvertSink():

    data = ConvertSink()
    test = convert_sinks(data)

    print(test['grid_specific']['heating'])
    print(test['grid_specific']['cooling'])

    """   
    
    Expected:
    [{'teo_equipment_name': 'ng_boiler_sink', 'input_fuel': 'grid_specific', 'output_fuel': 'sink_grid_specific_demand', 'equipment': ['hot_water_boiler'], 'max_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766058, 'turnkey_b': 4619.366306192671, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.03106451148390813, 'emissions': 0.22779730362698178, 'technologies': [{'object_type': 'equipment', 'equipment_sub_type': 'hot_water_boiler', 'fuel_type': 'natural_gas', 'fuel_properties': {'price': 0.03106451148390813, 'lhv_fuel': 13.1, 'excess_air_fuel': 1.0750000000000002, 'air_to_fuel_ratio': 17.2, 'co2_emissions': 0.209923664, 'density': 0.712}, 'supply_temperature': 85, 'return_temperature': 55, 'supply_capacity': 526, 'global_conversion_efficiency': 0.9215370887082585, 'data_teo': {'equipment': 'hot_water_boiler', 'fuel_type': 'natural_gas', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766054, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.03106451148390813, 'emissions': 0.2277973036269818}}]}, {'teo_equipment_name': 'oil_boiler_sink', 'input_fuel': 'grid_specific', 'output_fuel': 'sink_grid_specific_demand', 'equipment': ['hot_water_boiler'], 'max_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766058, 'turnkey_b': 4619.366306192671, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.065911153, 'emissions': 0.28894354037691566, 'technologies': [{'object_type': 'equipment', 'equipment_sub_type': 'hot_water_boiler', 'fuel_type': 'fuel_oil', 'fuel_properties': {'price': 0.065911153, 'lhv_fuel': 11.83, 'excess_air_fuel': 1.15, 'air_to_fuel_ratio': 14.6, 'co2_emissions': 0.266272189, 'density': 850.0}, 'supply_temperature': 85, 'return_temperature': 55, 'supply_capacity': 526, 'global_conversion_efficiency': 0.9215370887082585, 'data_teo': {'equipment': 'hot_water_boiler', 'fuel_type': 'fuel_oil', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766054, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.065911153, 'emissions': 0.28894354037691566}}]}, {'teo_equipment_name': 'biomass_boiler_sink', 'input_fuel': 'grid_specific', 'output_fuel': 'sink_grid_specific_demand', 'equipment': ['hot_water_boiler'], 'max_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766058, 'turnkey_b': 4619.366306192671, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.043199654, 'emissions': 0.3971625282201407, 'technologies': [{'object_type': 'equipment', 'equipment_sub_type': 'hot_water_boiler', 'fuel_type': 'biomass', 'fuel_properties': {'price': 0.043199654, 'lhv_fuel': 5.0, 'excess_air_fuel': 1.7, 'air_to_fuel_ratio': 10.76, 'co2_emissions': 0.366, 'density': 700.0}, 'supply_temperature': 85, 'return_temperature': 55, 'supply_capacity': 526, 'global_conversion_efficiency': 0.9215370887082585, 'data_teo': {'equipment': 'hot_water_boiler', 'fuel_type': 'biomass', 'max_input_capacity': 570.7854913764863, 'turnkey_a': 26.210226447766054, 'turnkey_b': 4619.366306192673, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 66.89128926534408, 'om_var': 0.043199654, 'emissions': 0.3971625282201407}}]}, {'teo_equipment_name': 'hp_sink', 'input_fuel': 'grid_specific', 'output_fuel': 'sink_grid_specific_demand', 'equipment': ['heat_pump'], 'max_capacity': 570.7854913764863, 'turnkey_a': 156.75830865938465, 'turnkey_b': 7206.975663369318, 'conversion_efficiency': 0.9215370887082585, 'om_fix': 338.7694514298439, 'om_var': 0.032088784576507955, 'emissions': 0.03773065496153149, 'technologies': [{'object_type': 'equipment', 'equipment_sub_type': 'heat_pump', 'fuel_type': 'electricity', 'fuel_properties': {'price': 0.0869, 'lhv_fuel': 'none', 'excess_air_fuel': 'none', 'air_to_fuel_ratio': 'none', 'co2_emissions': 0.255, 'density': 'none'}, 'supply_temperature': 85, 'return_temperature': 55, 'supply_capacity': 526, 'global_conversion_efficiency': 2.495625, 'data_teo': {'equipment': 'heat_pump', 'fuel_type': 'electricity', 'max_input_capacity': 210.7688454795893, 'turnkey_a': 424.5189464880308, 'turnkey_b': 7206.975663369303, 'conversion_efficiency': 2.495625, 'om_fix': 917.4253782988601, 'om_var': 0.0869, 'emissions': 0.10217881292261458}}]}]
    []
   
    """


