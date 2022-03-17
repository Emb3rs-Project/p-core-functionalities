

from ....Source.simulation.Convert.convert_sources import convert_sources
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import json
import os

script_dir = os.path.dirname(__file__)
data = json.load(open(os.path.join(script_dir, "sources_input.json")))


def testConvertSource():

    test = convert_sources(data, KB(kb))
    print(test['n_supply_list'])

    """
    Expected:
    [{'id': 1, 'stream_id': 15568, 'coords': [38.758848, -9.107296], 'cap': 952.2647966222223}, {'id': 2, 'stream_id': 94990, 'coords': [38.773896, -9.111059], 'cap': 397.68946522584594}]
    """





