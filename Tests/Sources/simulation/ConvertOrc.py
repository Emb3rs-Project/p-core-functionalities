
from ....Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from ....General.Simple_User.simple_user import simple_user


###########################################
# This is just to imitate the data treatment done by the platform. JUMP THIS PART.
###########################################
class Source_simplified():
    def __init__(self):
        # Input
        self.object_id = 5
        self.type_of_object = 'source'


        self.streams = [{'supply_temperature':400,'target_temperature':250,'fluid':'flue_gas','fluid_cp':1.3,'flowrate':321230,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[1,24]]},
                        {'supply_temperature': 360, 'target_temperature': 90, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 155897, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[1, 24]]}]

source = Source_simplified()
input_source_data = {}
input_source_data['platform'] = source.__dict__
industry_stream_test = simple_user(input_source_data)
stream_id = 1

for stream in industry_stream_test['streams']:
    stream['id'] = stream_id
    stream_id += 1

###########################################
###########################################


# IMPORTANT
class ConvertOrc:
    def __init__(self,streams):
        self.streams = streams
        self.consumer_type = 'non_household'
        self.location = [41,-8]
        self.get_best_number = 3

        # optional inputs
        # self.orc_T_evap = 300
        # self.orc_T_cond = 30



def testConvertORC():

    data = ConvertOrc(industry_stream_test['streams'])
    input_data = {}
    input_data['platform'] = data.__dict__
    test = convert_orc(input_data)

    for convert in test:
        print(convert)

    """ 
    Expected:
    {'ID': 3.0, 'streams_id': [1, 2], 'electrical_generation_nominal': 2402.734700802558, 'electrical_generation_yearly': 20226220.711355932, 'excess_heat_supply_capacity': 30911.031666666666, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 5156567.535654879, 'om_fix': 123413.15393904457, 'om_var': 0.00140277013688106, 'electrical_generation_yearly_turnkey': 0.25494468834505224, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.1, 'lifetime': 25}
    {'ID': 1.0, 'streams_id': [1], 'electrical_generation_nominal': 1352.5101371851756, 'electrical_generation_yearly': 11385430.334824808, 'excess_heat_supply_capacity': 17399.958333333332, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 3409168.5665233107, 'om_fix': 73434.29826967593, 'om_var': 0.0014273500602155122, 'electrical_generation_yearly_turnkey': 0.29943256128805507, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.1, 'lifetime': 25}
    {'ID': 2.0, 'streams_id': [2], 'electrical_generation_nominal': 1050.2245636173825, 'electrical_generation_yearly': 8840790.376531126, 'excess_heat_supply_capacity': 13511.073333333334, 'conversion_efficiency': 0.08612814824481275, 'turnkey': 2872272.7718427256, 'om_fix': 61227.593696480224, 'om_var': 0.0013711153873800829, 'electrical_generation_yearly_turnkey': 0.3248886863630991, 'co2_savings': 0.255, 'money_savings': 0.0869, 'discount_rate': 0.1, 'lifetime': 25}
     """
