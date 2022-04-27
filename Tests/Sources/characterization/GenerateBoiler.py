import json
import os
from ....Source.characterization.Generate_Equipment.generate_boiler import Boiler
from ....utilities.kb import KB
from ....utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/generate_boiler_test.json")))


def testGenerateBoiler():
    test = Boiler(data_test, KB(kb))

    if 260 < test.streams[2]['supply_temperature'] < 280:
        print('testGenerateBoiler - Everything Correct')
    else:
        print('testGenerateBoiler - Report to CF that something is odd')
