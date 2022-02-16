from ....General.Simple_User.simple_user import simple_user


class Industry():
    def __init__(self):
        # Input
        self.object_id = 2
        self.type_of_object = 'source'
        self.streams = [{
                            'supply_temperature':300, 'target_temperature':55, 'fluid':'flue_gas', 'fluid_cp':10,
                            'flowrate':10, 'saturday_on':1, 'sunday_on':1, 'shutdown_periods':[],
                            'daily_periods':[[10, 18]]},
                        {
                            'supply_temperature':500, 'target_temperature':55, 'fluid':'flue_gas', 'fluid_cp':10,
                            'flowrate':10, 'saturday_on':1, 'sunday_on':1, 'shutdown_periods':[],
                            'daily_periods':[[10, 18]]}]


def testOutflowSimplified():
    industry_data = Industry()
    industry_stream_test = simple_user(industry_data)
    print(industry_stream_test[0]['flowrate'])


    """
    print(industry_stream_test[0]['flowrate'])

    10
    """

testOutflowSimplified()
