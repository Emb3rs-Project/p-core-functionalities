from ....src.Source.simulation.Heat_Recovery.convert_pinch_isolated_streams import convert_pinch_isolated_streams
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb
import os
import json


script_dir = os.path.dirname(__file__)


def testConvertPinchIsolated():

    data_test = json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_raw.json")))

    test = convert_pinch_isolated_streams(data_test, KB(kb))


    print("Convert Pinch with Isolated Stream run Successfully")
