from ....General.Simple_User.simple_user import simple_user


class Industry():
    def __init__(self):
        # Input
        self.object_id = 2
        self.type_of_object = 'sink'
        self.streams = [
            {
                'supply_temperature': 10,
                'target_temperature': 55,
                'fluid': 'water',
                'fluid_cp': 10,
                'flowrate': 10,
                'saturday_on': 1, 'sunday_on': 1,
                'shutdown_periods': [],
                'daily_periods': [[10, 18]]},
            {
                'supply_temperature': 10,
                'target_temperature': 55,
                'fluid': 'water',
                'fluid_cp': 10,
                'flowrate': 10,
                'saturday_on': 1,
                'sunday_on': 1,
                'shutdown_periods': [],
                'daily_periods': [[10, 18]]
            }
        ]


def testIndustry():
    industry_data = Industry()
    input_data = {}
    input_data['platform'] = industry_data.__dict__

    industry_stream_test = simple_user(input_data)
    print(industry_stream_test['streams'][0]['stream_type'])

    """    
    Expected:
    'inflow'
    """
