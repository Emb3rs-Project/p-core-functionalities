from ....Source.characterization.Process.process import Process
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import os
import json

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/process_test.json")))


def testProcess():
    process = Process(data_test, KB(kb))

    result = ['startup',
              'maintenance',
              'inflow',
              'inflow',
              'outflow']

    error = 0
    for index, stream in enumerate(process.streams):

        if stream['stream_type'] != result[index]:
            error = 1

    if error == 0:
        print('testProcess - Everything Correct')
    else:
        print('testProcess - Report to CF that something is odd')
