
from ....Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from ....General.Simple_User.simple_user import simple_user


###########################################
# This is just to imitate the data treatment done by the platform. JUMP THIS PART.
###########################################
class Source_simplified():
    def __init__(self):
        # Input
        # Input
        self.object_id = 5
        self.type_of_object = 'source'


        self.streams = [{'supply_temperature':400,'target_temperature':250,'fluid':'flue_gas','fluid_cp':1.3,'flowrate':321230,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[1,24]]},
                        {'supply_temperature': 360, 'target_temperature': 90, 'fluid': 'flue_gas', 'fluid_cp': 1.3,
                            'flowrate': 155897, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods': [[1, 24]]}]

source = Source_simplified()
industry_stream_test = simple_user(source)
stream_id = 1

for stream in industry_stream_test:
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



def testConvertORC():

    data = ConvertOrc(industry_stream_test)
    test = convert_orc(data)

    for convert in test:
        print(convert)

    """
    for convert in test:
        print(convert['streams_id'])
        
    Expected:
    [1, 2]
    [1]
    [2]
     """
