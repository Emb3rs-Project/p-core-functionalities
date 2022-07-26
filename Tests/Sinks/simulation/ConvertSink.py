from ....src.Sink.simulation.convert_sinks import convert_sinks
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "test_files/convert_sinks_input.json")))


def testConvertSink():

    test = convert_sinks(data, KB(kb))

    if test['all_sinks_info']['grid_specific'][0]['equipment'][0] == 'hot_water_boiler' and test['all_sinks_info']['grid_specific'][0]['max_capacity'] == 5279.288:
        print('Convert SINK Test - Everything Correct')
    else:
        print('Convert SINK Test - Report to CF that something is odd')

