from ....src.General.Simple_User.simple_user import simple_user
import json
import os

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/source_simple_industry_test.json")))


def testSourceSimpleUser():
    test = simple_user(data_test)

    if test['streams'][0]['flowrate'] == 10:
        print('testSourceSimpleUser - Everything Correct')
    else:
        print('testSourceSimpleUser - Report to CF that something is odd')


