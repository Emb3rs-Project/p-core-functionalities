
from ....Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from ....utilities.kb import KB
from ....utilities.kb_data import kb

import json
import os

script_dir = os.path.dirname(__file__)
data_test_1 = json.load(open(os.path.join(script_dir, "orc_1_input.json")))
data_test_2 = json.load(open(os.path.join(script_dir, "orc_2_input.json")))

def testConvertORC():

    # TEST 1
    test_1 = convert_orc(data_test_1, KB(kb))

    # TEST 2
    test_2 = convert_orc(data_test_2, KB(kb))

    validation_data_test_1 = [{'ID': 3.0, 'streams_id': [1, 2], 'electrical_generation_nominal': 2402.734700802558, 'electrical_generation_yearly': 20226220.711355932, 'excess_heat_supply_capacity': 30911.031666666666, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 5156567.535654879, 'om_fix': 123413.15393904457, 'om_var': 0.00140277013688106, 'electrical_generation_yearly_turnkey': 0.25494468834505224, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.04, 'lifetime': 25}, {'ID': 1.0, 'streams_id': [1], 'electrical_generation_nominal': 1352.5101371851756, 'electrical_generation_yearly': 11385430.334824808, 'excess_heat_supply_capacity': 17399.958333333332, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 3409168.5665233107, 'om_fix': 73434.29826967593, 'om_var': 0.0014273500602155122, 'electrical_generation_yearly_turnkey': 0.29943256128805507, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.04, 'lifetime': 25}, {'ID': 2.0, 'streams_id': [2], 'electrical_generation_nominal': 1050.2245636173825, 'electrical_generation_yearly': 8840790.376531126, 'excess_heat_supply_capacity': 13511.073333333334, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 2872272.7718427256, 'om_fix': 61227.593696480224, 'om_var': 0.0013711153873800829, 'electrical_generation_yearly_turnkey': 0.3248886863630991, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.04, 'lifetime': 25}]
    validation_data_test_2 = [{'ID': 1.0, 'streams_id': [1], 'electrical_generation_nominal': 946.1809645974304, 'electrical_generation_yearly': 7964951.359981169, 'excess_heat_supply_capacity': 4639.988888888888, 'conversion_efficiency': 0.22594880847308033, 'turnkey': 2503986.7667533075, 'om_fix': 39572.92154883344, 'om_var': 0.00045554673762596306, 'electrical_generation_yearly_turnkey': 0.3143756507207632, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.04, 'lifetime': 25}, {'ID': 2.0, 'streams_id': [1, 2], 'electrical_generation_nominal': 946.1809645974304, 'electrical_generation_yearly': 7964951.359981169, 'excess_heat_supply_capacity': 4639.988888888888, 'conversion_efficiency': 0.22594880847308033, 'turnkey': 2503986.7667533075, 'om_fix': 39572.92154883344, 'om_var': 0.00045554673762596306, 'electrical_generation_yearly_turnkey': 0.3143756507207632, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.04, 'lifetime': 25}]

    error = 0
    for index,conversion in enumerate(test_1):
        if conversion != validation_data_test_1[index]:
            error = 1

    if error == 0:
        print('Convert ORC Test 1 - Everything Correct')
    else:
        print('Convert ORC Test 1 - Report to CF that something is odd')

    error = 0
    for index,conversion in enumerate(test_2):
        if conversion != validation_data_test_2[index]:
            error = 1

    if error == 0:
        print('Convert ORC Test 2 - Everything Correct')
    else:
        print('Convert ORC Test 2 - Report to CF that something is odd')


