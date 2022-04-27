from ....Source.characterization.Generate_Equipment.generate_cooling_equipment import Cooling_Equipment
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import os
import json

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/generate_cooling_equipment_test.json")))


def testGenerateCoolingEquipment():
    test = Cooling_Equipment(data_test, KB(kb))

    if 5900 < test.streams[0]['capacity'] < 6000:
        print('testGenerateCoolingEquipment - Everything Correct')
    else:
        print('testGenerateCoolingEquipment - Report to CF that something is odd')
