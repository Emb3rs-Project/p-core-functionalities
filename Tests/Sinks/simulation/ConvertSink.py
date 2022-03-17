

from ....Sink.simulation.Convert.convert_sinks import convert_sinks
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "sinks_input.json")))


def testConvertSink():
    test = convert_sinks(data, KB(kb))

    print(test)

    """       
    Expected:
    {'all_sinks_info': {'sink_group_grid_supply_temperature': 100, 'sink_group_grid_return_temperature': 70, 'grid_specific': {'heating': [{'teo_equipment_name': 'sink-grid_specific-grid_specific-ng_boiler_sink', 'output': 1, 'input_fuel': None, 'output_fuel': 'dhn_water_supply', 'equipment': ['hot_water_boiler'], 'max_capacity': 5398.305165783063, 'turnkey_a': 7.4728694961333755, 'turnkey_b': 12456.141503842795, 'conversion_efficiency': 0.9681734141665852, 'om_fix': 19.07155880946723, 'om_var': 0.031234430124559006, 'emissions': 0.21682444583618804, 'technologies': [{'object_type': 'equipment', 'equipment_sub_type': 'hot_water_boiler'    """

    """"""

