from ....Sink.characterization.Building.greenhouse import greenhouse


class Greenhouse:
    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 41.1045
        self.longitude = -8.3539
        self.building_orientation = "S"
        self.greenhouse_orientation = "greenhouse"
        self.building_efficiency = 1
        self.width = 50
        self.length = 23
        self.height = 3  # greenhouse height [m]
        self.shutdown_periods = []
        self.hours_lights_needed = 15  # number of hours plants needed with light
        self.daily_periods = [[0, 24]]  # heating needed all day
        self.lights_on = 0  # on
        self.T_cool_on = 35  # cooling start temperature working hours [ºC]
        self.T_heat_on = 18  # heating start temperature working hours [ºC]
        self.building_efficiency = 1  # show options of greenhouse efficiency - 1=tight sealed greenhouse; 2=medium; 3=loose

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values        self.target_temperature_heat = 50
        self.supply_temperature_heat = 30
        self.saturday_on = 1  # heat on saturdays - assumed greenhouse works everyday
        self.sunday_on = 1  # heat on sunday - assumed greenhouse works everyday
        self.power_lights = 20  # [W/m2]
        self.u_cover = 6.5  # [W/m2]
        self.leaf_area_index = 1
        self.rh_air = 0.70  # relative humidity
        self.indoor_air_speed = 0.1  # [m/s]
        self.leaf_length = 0.027  # [m]
        self.tau_cover_long_wave_radiation = 0.3
        self.emissivity_cover_long_wave_radiation = 0.2
        self.tau_cover_solar_radiation = 0.75

        # value f_c
        # maybe show equation to the user and link to article regarding infiltrations computation
        # link: https: // doi.org / 10.1016 / j.compag.2018.04.025
        # assumptions: f_t = 0.16;  c_w = 0.22
        # equation: total_cover_area * f_c * math.sqrt( c_w ** 2 * wind_speed + f_t ** 2 * (abs(T_interior - T_exterior)))  # [m3/s]
        # user can introduce f_c that he wants to
        self.f_c = 2.5 * 10 ** (-4)  # factor to estimate building infiltrations


def testGreenhouse():

    data = Greenhouse()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = greenhouse(input_data)

    print(test)
    """"
    Expected:
    [34360.06786579071, 27126.003499951665, 27565.57197713766, 21650.832164568514, 14797.813745460455, 10800.824021053113, 6460.46181873828, 7254.042281065299, 9533.84325632785, 17493.78056170256, 34676.07498035828, 36286.162510339]
    """

