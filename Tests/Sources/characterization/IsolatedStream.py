from ....General.Simple_User.isolated_stream import isolated_stream
import json
import os

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir, "test_files/isolated_stream_1.json")))

def testIsolatedStream():
    test = isolated_stream(data_test)





