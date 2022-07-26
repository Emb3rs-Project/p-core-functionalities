from ....src.General.Simple_User.simple_user import simple_user
import os
import json

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/sink_simple_user.json")))


def testSinkSimpleUser():

    test = simple_user(data_test)

    if test['streams'][0]['capacity'] == 2.0416666666666665:
        print('testSinkSimpleUser - Everything Correct')
    else:
        print('testSinkSimpleUser - Report to CF that something is odd')

