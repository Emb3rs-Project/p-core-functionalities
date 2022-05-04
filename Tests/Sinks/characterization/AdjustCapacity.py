import os
import json
from ....Sink.characterization.Building.adjust_capacity import adjust_capacity

script_dir = os.path.dirname(__file__)
data_hot_stream = json.load(open(os.path.join(script_dir, "test_files/adjust_cap_hot_stream.json")))
data_cold_stream = json.load(open(os.path.join(script_dir, "test_files/adjust_cap_cold_stream.json")))

def testAdjustCapacity():

    # Adjust Capacity
    # hot stream
    test = adjust_capacity(data_hot_stream)
    if sum(test['monthly_generation']) == 66945.80266101885:
        print('testAdjustCapacity hot stream- Everything Correct')
    else:
        print('testAdjustCapacity hot stream- Report to CF that something is odd')

    # cold stream
    test = adjust_capacity(data_cold_stream)

    if sum(test['monthly_generation']) == 50000:
        print('testAdjustCapacity cold stream - Everything Correct')
    else:
        print('testAdjustCapacity cold stream - Report to CF that something is odd')



