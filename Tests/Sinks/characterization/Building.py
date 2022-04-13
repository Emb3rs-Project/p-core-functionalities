from ....Sink.characterization.Building.building import building
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data_1 = json.load(open(os.path.join(script_dir, "building_paper_input.json")))
data_2 = json.load(open(os.path.join(script_dir, "building_inegi_corpo_input.json")))

def testBuilding():

    # Paper
    test = building(data_1, KB(kb))

    value_heat = int(sum(test['hot_stream']['monthly_generation'])/(data_1['platform']['number_floor'] * data_1['platform']['length_floor'] * data_1['platform']['width_floor']))
    value_cool = int(sum(test['cold_stream']['monthly_generation'])/(data_1['platform']['number_floor'] * data_1['platform']['length_floor'] * data_1['platform']['width_floor']))

    if int(value_heat) == 35 and int(value_cool) == 20:
        print('Building Test 1 - Everything Correct')
    else:
        print('Building Test 1 - Report to CF that something is odd')


    # Inegi Corpo
    test = building(data_2, KB(kb))

    for i in test['hot_stream']['monthly_generation']:
        i /= 0.9

    value_heat = sum(test['hot_stream']['monthly_generation'])
    value_cool = sum(test['cold_stream']['monthly_generation'])

    if 15000 < int(value_heat) < 16000 and 15000 < int(value_cool) < 16000:
        print('Building Test 2 - Everything Correct')
    else:
        print('Building Test 2 - Report to CF that something is odd')

