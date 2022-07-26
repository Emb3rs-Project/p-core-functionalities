from ....src.Source.simulation.Convert.convert_sources import convert_sources
from ....src.utilities.kb import KB
from ....src.utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "test_files/convert_sources_test.json")))


def testConvertSource():
    test = convert_sources(data, KB(kb))

    if test['all_sources_info'][0]['streams_converted'][0]['conversion_technologies'][0][
        'equipment'] == ['hx_economizer', 'circulation_pumping', 'hx_plate', 'circulation_pumping']:
        print('testConvertSource - Everything Correct')
    else:
        print('testConvertSource - Report to CF that something is odd')
