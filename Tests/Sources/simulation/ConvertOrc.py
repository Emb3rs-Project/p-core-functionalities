from ....src.Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data_test_1 = json.load(open(os.path.join(script_dir, "test_files/orc_test_1.json")))
data_test_2 = json.load(open(os.path.join(script_dir, "test_files/orc_test_2.json")))


def testConvertORC():
    # TEST 1
    test_1 = convert_orc(data_test_1, KB(kb))



    # TEST 2
   # test_2 = convert_orc(data_test_2, KB(kb))

    print("Convert ORC run successfully")