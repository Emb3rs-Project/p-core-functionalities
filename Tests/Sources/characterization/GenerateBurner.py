import json
import os
from ....Source.characterization.Generate_Equipment.generate_burner import Burner
from ....utilities.kb import KB
from ....utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/generate_burner_test.json")))


def testGenerateBurner():
    test = Burner(data_test, KB(kb))

    if 500 < test.streams[0]['capacity'] < 600:
        print('testGenerateBurner - Everything Correct')
    else:
        print('testGenerateBurner - Report to CF that something is odd')
