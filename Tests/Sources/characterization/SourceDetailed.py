from ....Source.characterization.source_detailed import source_detailed
import json
import os
from ....utilities.kb import KB
from ....utilities.kb_data import kb

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/source_detailed.json")))


def testSourceDetailedUser():
    test = source_detailed(data_test, KB(kb))

    result = ['startup',
              'maintenance',
              'inflow',
              'inflow',
              'outflow']

    error = 0

    for object in test:
        if object.object_type == 'process':
            for index, stream in enumerate(object.streams):
                if stream['stream_type'] != result[index]:
                    error = 1

        elif object.object_type == 'boiler':
            if not 260 < test.streams[2]['supply_temperature'] < 280:
                error = 1

        elif object.object_type == 'burner':
            if not 500 < test.streams[0]['capacity'] < 600:
                error = 1

        elif object.object_type == 'cooling_equipment':
            if not 5900 < test.streams[0]['capacity'] < 6000:
                error = 1

        elif object.object_type == 'chp':
            if not 200 < test.streams[0]['capacity'] < 220:
                error = 1

    if error == 0:
        print('testSourceDetailedUser - Everything Correct')
    else:
        print('testSourceDetailedUser - Report to CF that something is odd')


