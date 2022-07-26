from ....src.Sink.characterization.building import building
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data_1 = json.load(open(os.path.join(script_dir, "test_files/building_paper_input.json")))

def testBuilding():

    # Paper
    test = building(data_1, KB(kb))

    value_heat = int(sum(test['streams'][0]['monthly_generation'])/(data_1['platform']['number_floor'] * data_1['platform']['length_floor'] * data_1['platform']['width_floor']))
    value_cool = int(sum(test['streams'][1]['monthly_generation'])/(data_1['platform']['number_floor'] * data_1['platform']['length_floor'] * data_1['platform']['width_floor']))

    if int(value_heat) == 35 and int(value_cool) == 20:
        print('Building Test 1 - Everything Correct')
    else:
        print('Building Test 1 - Report to CF that something is odd')
#
