import os
import json
from module.General.Simple_User.su_adjust_capacity import su_adjust_capacity

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/su_adjust_capacity.json")))

def testSUAdjustCapacity():

    # Adjust Capacity
    test = su_adjust_capacity(data_test)

    print(test)


