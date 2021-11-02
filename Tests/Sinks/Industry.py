from ...General.Simple_User.simple_user import simple_user


class Industry():
    def __init__(self):
        # Input
        self.object_id = 2
        self.type_of_object = 'sink'
        self.streams = [{'supply_temperature': 10, 'target_temperature': 55, 'fluid': 'water', 'fluid_cp': 10, 'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods':[[10, 18]]},
                        {'supply_temperature': 10, 'target_temperature': 55, 'fluid': 'water', 'fluid_cp': 10, 'flowrate': 10, 'saturday_on': 1, 'sunday_on': 1, 'shutdown_periods': [], 'daily_periods':[[10, 18]]}]


def testIndustry():
    # SINK -------------------------------------------------
    # Industry
    # user can create multiples industry streams for one industry by running the same code -> same sink id must be used
    industry_data = Industry()
    industry_stream_test = simple_user(industry_data)

    print(industry_stream_test)
