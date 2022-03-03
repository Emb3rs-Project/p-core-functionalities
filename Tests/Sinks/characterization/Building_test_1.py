from ....Sink.characterization.Building.building import building
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class Building_test_1():

    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 51.153
        self.longitude = -0.182
        self.building_orientation = 'S'
        self.building_type = 'office'
        self.number_floor = 3  # number of floors
        self.width_floor = 32
        self.length_floor = 16
        self.height_floor = 3.5  # floor height [m]
        self.ratio_wall_N = 0.5  # wall area fraction
        self.ratio_wall_S = 0.5
        self.ratio_wall_E = 0.5
        self.ratio_wall_W = 0.5
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = []
        self.daily_periods = [[7, 19]]
        self.space_heating_type = 1  # Space heating system - 0=Conventional, 1=Low temperature
        self.T_cool_on = 24  # cooling start temperature working hours [ºC]
        self.T_heat_on = 22  # heating start temperature working hours [ºC]
        self.T_off_min = 12  # heating start temperature off peak [ºC]
        self.T_off_max = 28  # cooling start temperature off peak [ºC


def testBuilding_1():

    # Office/Hotel/Residential Building
    data_building = Building_test_1()
    input_data = {}
    input_data['platform'] = data_building.__dict__
    test = building(input_data, KB(kb))

    print(sum(test['hot_stream']['monthly_generation'])/(input_data['platform']['number_floor'] * input_data['platform']['length_floor'] * input_data['platform']['width_floor']))

    print(sum(test['cold_stream']['monthly_generation'])/(input_data['platform']['number_floor'] * input_data['platform']['length_floor'] * input_data['platform']['width_floor']))
