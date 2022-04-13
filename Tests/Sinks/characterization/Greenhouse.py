from ....Sink.characterization.Building.greenhouse import greenhouse
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "greenhouse_simple_input.json")))

def testGreenhouse():

    test = greenhouse(data)
    value_heat = sum(test['hot_stream']['monthly_generation'])

    if 80000 < int(value_heat) < 90000:
        print('Greenhouse Test - Everything Correct')
    else:
        print('Greenhouse Test - Report to CF that something is odd')
