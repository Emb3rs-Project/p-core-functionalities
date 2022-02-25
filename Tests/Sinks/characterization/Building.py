from ....Sink.characterization.Building.building import building
from ....utilities.kb import KB
from ....utilities.kb_data import kb

class Building():

    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 51.153
        self.longitude = -0.182
        self.country = 'Portugal'
        self.building_orientation = 'S'
        self.building_type = 'office'
        if self.building_type == 'hotel':
            self.number_rooms = 15  # number of rooms per floor
        else:
            self.number_rooms = 0 # does not matter
        self.number_person_per_floor = 100  # number of occupants per floor
        self.number_floor = 3  # number of floors
        self.width_floor = 32
        self.length_floor = 16
        self.area_floor = self.width_floor * self.length_floor  # floor space area [m2]
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
        # show options
        if self.space_heating_type == 0:
            self.target_temperature_heat = 75
            self.supply_temperature_heat = 45
        else:
            self.target_temperature_heat = 50
            self.supply_temperature_heat = 30

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.T_cool_on = 24  # cooling start temperature working hours [ºC]
        self.T_heat_on = 22  # heating start temperature working hours [ºC]
        self.T_off_min = 12  # heating start temperature off peak [ºC]
        self.T_off_max = 28  # cooling start temperature off peak [ºC]
        self.emissivity_wall = 0.9
        self. emissivity_glass = 0.9

        self.target_temperature_cool = 7  # Cooling
        self.supply_temperature_cool = 12
        # self.u_wall, self.u_roof, self.u_glass, self.u_floor,self.tau_glass, self.alpha_wall, self.alpha_floor, self.alpha_glass, self.cp_wall, self.cp_floor, self.cp_roof,  self.air_change_hour = building_properties(self.country,self.building_type)

        if self.building_type == 'residential':
            self.Q_gain_per_floor = 5 * self.area_floor  # occupancy and appliances heat gains [W]
            self.vol_dhw_set = 0.03 * self.number_person_per_floor  # daily dwelling DHW consumption per floor [m3]
            self.renewal_air_per_person = 0  # renewal fresh air [m3/s]

        elif self.building_type == 'hotel':
            self.number_person_per_floor = 2 * self.number_rooms  # number of rooms per floor
            self.vol_dhw_set = 0.03 * self.number_person_per_floor  # daily dwelling DHW consumption [m3]
            self.Q_gain_per_floor = 5 * self.area_floor  # occupancy and appliances heat gains [W]
            self.renewal_air_per_person = 0  # renewal fresh air [m3/s]

        else:
            self.number_person_per_floor = round(self.area_floor / 9)  # number of occupants per floor (9m2 per occupant)
            self.vol_dhw_set = 0
            self.Q_gain_per_floor = self.number_person_per_floor * 108 + (15 + 12) * self.area_floor  # occupancy and appliances heat gains [W]
            self.renewal_air_per_person = 10 * 10 ** (-3)  # [m3/s]


def testBuilding():

    # Office/Hotel/Residential Building
    data_building = Building()
    input_data = {}
    input_data['platform'] = data_building.__dict__
    test = building(input_data, KB(kb))

    print(test)

    """
    print(test['streams'][0]['monthly_generation'])

    Expected:
    [9911.371909940874, 5770.759849320614, 3920.523099102963, 1973.6469068373362, 99.94233373898948, 10.48881136773229, 12.080701917663642, 11.964988150873587, 212.90883342474393, 1007.3412837863171, 2748.7041973066575, 6916.810412898163]
    """

