from ....Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import os
import json

# IMPORTANT
### OPTION 1 - just pinch analysis (energy optimization) - INPUT: isolated streams (example below)
### OPTION 2 - pinch analysis with processes (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments
### OPTION 3 - pinch analysis with processes and isolated streams (co2,energy,cost optmization - 3 best solutions of each) - INPUT:processes, equipments and isolated streams
### OPTION 4 - equipment internal optimization (co2,energy,cost - 1 solution of each) - INPUT: only one equipment at a time

script_dir = os.path.dirname(__file__)

def isolatedstreams(option):
    data_isolated_streams = {
        1: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_1.json"))),
        2: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_2.json"))),
        3: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_3.json"))),
        4: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_4.json"))),
        # pag.323
        5: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_5.json"))),
        6: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_6.json"))),
        7: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_7.json"))),
        # https://processdesign.mccormick.northwestern.edu/index.php/Pinch_analysis
        8: json.load(open(os.path.join(script_dir, "test_files/pinch_isolated_streams_test_8.json")))
        # pag.338
    }
    return data_isolated_streams[option]

def equipment_and_processes():
    return json.load(open(os.path.join(script_dir, "test_files/pinch_process_equipment.json")))

def equipment():
    return json.load(open(os.path.join(script_dir, "test_files/pinch_equipment.json")))

def equipment_process_isolated_stream():
    return json.load(open(os.path.join(script_dir, "test_files/pinch_process_equipment_isolated_stream.json")))


def testConvertPinch():

    import time
    t0 = time.time()


    option = 1

    # OPTION 1 - test isolated streams
    if option == 1:
        data_test = isolatedstreams(2)

        data_test = json.load(open(os.path.join(script_dir, "test_files/pinch_detailed.json")))

        data_test = json.load(open(os.path.join(script_dir, "test_files/pinch_detailed_workshop.json")))

        test = convert_pinch(data_test, KB(kb))

        file = open("sampleaaaaaaa.html", "w")
        file.write(test['report'])
        file.close()




    # OPTION 2 - test processes, equipments
    elif option ==2:
        data_test = equipment_and_processes()
        test = convert_pinch(data_test, KB(kb))

    # OPTION 3 - test processes, equipments and isolated streams
    elif option == 3:
        data_test = equipment_process_isolated_stream()
        test = convert_pinch(data_test, KB(kb))

    # OPTION 4 - test equipment (one at a time)
    elif option == 4:
        data_test = equipment()
        test = convert_pinch(data_test, KB(kb))


    t1 = time.time()
    total = t1 - t0

    print('time simulation [s]:', total)


