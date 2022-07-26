from ....src.Source.characterization.source_detailed import source_detailed
import json
import os
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
#data_test = json.load(open(os.path.join(script_dir, "test_files/source_detailed.json")))

data_test = json.load(open(os.path.join(script_dir, "test_files/source_detailed_workshop.json")))

def testSourceDetailedUser():
    test = source_detailed(data_test, KB(kb))

    print('Source Detailed Run Successfully')

    #result = ['startup',
    #          'maintenance',
    #          'inflow',
    #          'inflow',
    #          'outflow']


    #test = [ob.__dict__ if type(ob) is not dict else ob for ob in test ]
#
#
    #pinch_data = {
    #    "platform": {
    #        "streams_to_analyse": [1, 4, 13, 14],
    #        "all_input_objects": test,
    #        "pinch_delta_T_min": 20,
    #        "location": [
    #            48.864716,
    #            2.349014
    #        ]
    #    }
    #}
#
    #with open("pinch_detailed_workshop.json", "w") as outfile:
    #    json.dump(pinch_data, outfile)


