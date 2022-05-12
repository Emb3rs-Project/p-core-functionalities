import os
import json
from module.Sink.characterization.building_adjust_capacity import building_adjust_capacity

script_dir = os.path.dirname(__file__)
data_hot_stream = json.load(open(os.path.join(script_dir, "test_files/adjust_cap_hot_stream.json")))
data_cold_stream = json.load(open(os.path.join(script_dir, "test_files/adjust_cap_cold_stream.json")))

def testBuildingAdjustCapacity():

    # Adjust Capacity
    # hot stream
    test = building_adjust_capacity(data_hot_stream)

    if sum(test['monthly_generation']) == 66945.79999999999:
        print('testAdjustCapacity hot stream- Everything Correct')
    else:
        print('testAdjustCapacity hot stream- Report to CF that something is odd')

    # cold stream
    test = building_adjust_capacity(data_cold_stream)
    if sum(test['monthly_generation']) == 49999.99:
        print('testAdjustCapacity cold stream - Everything Correct')
    else:
        print('testAdjustCapacity cold stream - Report to CF that something is odd')



