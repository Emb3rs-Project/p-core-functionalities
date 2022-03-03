from ....Sink.characterization.Building.building import building
from ....utilities.kb import KB
from ....utilities.kb_data import kb
import math

class Building_test_2():

    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 41.1045
        self.longitude = -8.3539
        self.building_orientation = 'S'
        self.building_type = 'office'
        self.number_floor = 10  # number of floors
        self.width_floor = math.sqrt(285)
        self.length_floor = math.sqrt(285)
        self.height_floor = 2.7  # floor height [m]
        self.ratio_wall_N = 0.9  # wall area fraction
        self.ratio_wall_S = 0.3
        self.ratio_wall_E = 0.3
        self.ratio_wall_W = 0.9
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = []
        self.daily_periods = [[7, 19]]
        self.space_heating_type = 1  # Space heating system - 0=Conventional, 1=Low temperature
        self.T_cool_on = 25
        self.T_heat_on = 22
        self.T_off_min = 0
        self.T_off_max = 50


def testBuilding_2():

    # Office/Hotel/Residential Building
    data_building = Building_test_2()
    input_data = {}
    input_data['platform'] = data_building.__dict__
    test = building(input_data, KB(kb))

    print(test['hot_stream']['monthly_generation'])

    print(test['cold_stream']['monthly_generation'])
