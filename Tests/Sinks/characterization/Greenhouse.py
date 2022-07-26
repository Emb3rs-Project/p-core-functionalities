from ....src.Sink.characterization.greenhouse import greenhouse
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "test_files/greenhouse_simple_input.json")))

def testGreenhouse():

    test = greenhouse(data)

    value_heat = sum(test['streams'][0]['monthly_generation'])

    if 60233 < int(value_heat) < 62233:
        print('Greenhouse Test - Everything Correct')
    else:
        print('Greenhouse Test - Report to CF that something is odd')
