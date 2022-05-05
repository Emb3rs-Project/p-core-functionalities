from module.Sink.characterization.building import building
from module.utilities.kb import KB
from module.utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data_2 = json.load(open(os.path.join(script_dir, "building_inegi_corpo_input.json")))

def testBuilding_2():

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
