from ....src.Source.characterization.source_detailed import source_detailed
import json
import os
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/source_detailed.json")))
data_test = json.load(open(os.path.join(script_dir, "test_files/source_detailed_workshop.json")))

def testSourceDetailedUser():
    test = source_detailed(data_test, KB(kb))

    print('Source Detailed Run Successfully')

