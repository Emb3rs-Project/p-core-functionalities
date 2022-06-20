from ....Source.simulation.Heat_Recovery.pinch_isolated_streams import pinch_isolated_streams
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import os
import json


script_dir = os.path.dirname(__file__)


def testConvertPinchIsolated():

    data_test = json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_raw.json")))

    test = pinch_isolated_streams(data_test, KB(kb))


    file = open("sampleaaaaaaa.html", "w")
    file.write(test['report'])
    file.close()