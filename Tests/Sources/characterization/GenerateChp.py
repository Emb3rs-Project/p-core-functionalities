import json
import os
from ....Source.characterization.Generate_Equipment.generate_chp import Chp
from ....utilities.kb import KB
from ....utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/generate_chp_test.json")))


def testGenerateChp():
    test = Chp(data_test, KB(kb))

    if 200 < test.streams[0]['capacity'] < 220:
        print('testGenerateChp - Everything Correct')
    else:
        print('testGenerateChp - Report to CF that something is odd')
