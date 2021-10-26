"""





"""



from Sink.characterization.Building.building import building
from Sink.characterization.Building.greenhouse import greenhouse
from Sink.characterization.Industry.industry import industry
from KB_General.building_properties import building_properties

class Greenhouse():
    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 41.1045
        self.longitude = -8.3539
        self.building_orientation = 'S'
        self.building_type = 'greenhouse'
        self.building_efficiency = 1
        self.width = 50
        self.length = 23
        self.height_floor = 3  # greenhouse height [m]
        self.shutdown_periods = []
        self.hours_lights_needed = 15  # number of hours plants needed with light
        self.daily_periods = [[0, 24]] # heating needed all day
        self.lights_on = 0  # on
        self.T_cool_on = 35  # cooling start temperature working hours [ºC]
        self.T_heat_on = 10  # heating start temperature working hours [ºC]

        #show options of greenhouse efficiency - 1=tight sealed greenhouse; 2=medium; 3=loose
        self.building_efficiency = 1

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values        self.target_temperature_heat = 50
        self.supply_temperature_heat = 30
        self.saturday_on = 1 # heat on saturdays - assumed greenhouse works everyday
        self.sunday_on = 1 # heat on sunday - assumed greenhouse works everyday
        self.power_lights = 20  # [W/m2]
        self.u_cover = 6  # [W/m2]
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
        # assumeptions: f_t = 0.16;  c_w = 0.22
        # equation: total_cover_area * f_c * math.sqrt( c_w ** 2 * wind_speed + f_t ** 2 * (abs(T_interior - T_exterior)))  # [m3/s]
        # user can introduce f_c that he wants to
        self.f_c = 2.5 * 10 ** (-4) # factor to estimate building infiltrations

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
        self.width = 32
        self.length = 16
        self.area_floor = self.width * self.length  # floor space area [m2]
        self.height_floor = 3.5  # floor height [m]
        self.ratio_wall_N = 0.5  # wall area fraction
        self.ratio_wall_S = 0.5
        self.ratio_wall_E = 0.5
        self.ratio_wall_W = 0.5
        self.saturday_on = 0
        self.sunday_on = 0
        self.shutdown_periods = []
        self.daily_periods = [[7, 19]]

        # show options
        if self.space_heating_type == 0:
            self.target_temperature_heat = 75
            self.supply_temperature_heat = 45
        else:
            self.target_temperature_heat = 50
            self.supply_temperature_heat = 30

        ###################
        # Optional/Expert User inputs -  should be shown on the platform as default values
        self.space_heating_type = 1  # Space heating system - 0=Conventional, 1=Low temperature
        self.T_cool_on = 24  # cooling start temperature working hours [ºC]
        self.T_heat_on = 22  # heating start temperature working hours [ºC]
        self.T_off_min = 12  # heating start temperature off peak [ºC]
        self.T_off_max = 28  # cooling start temperature off peak [ºC]

        self.target_temperature_cool = 7  # Cooling
        self.supply_temperature_cool = 12
        self.u_wall, self.u_roof, self.u_glass, self.u_floor,self.tau_glass, self.alpha_wall, self.alpha_floor, self.alpha_glass, self.cp_wall, self.cp_floor, self.cp_roof,  self.air_change_hour = building_properties(self.country,self.building_type)

        if self.building_type == 'residential':
            self.Q_gain = 5 * self.area_floor  # occupancy and appliances heat gains [W]
            self.vol_dhw_set = 0.03 * self.number_person_per_floor  # daily dwelling DHW consumption per floor [m3]
            self.renewal_air_per_person = 0  # renewal fresh air [m3/s]

        elif self.building_type == 'hotel':
            self.number_person_per_floor = 2 * self.number_rooms  # number of rooms per floor
            self.vol_dhw_set = 0.03 * self.number_person_per_floor  # daily dwelling DHW consumption [m3]
            self.Q_gain = 5 * self.area_floor  # occupancy and appliances heat gains [W]
            self.renewal_air_per_person = 0  # renewal fresh air [m3/s]

        else:
            self.number_person_per_floor = round(self.area_floor / 9)  # number of occupants per floor (9m2 per occupant)
            self.vol_dhw_set = 0
            self.Q_gain = self.number_person_per_floor * 108 + (15 + 12) * self.area_floor  # occupancy and appliances heat gains [W]
            self.renewal_air_per_person = 10 * 10 ** (-3)  # [m3/s]

class Industry_Process():
    def __init__(self):
        # Input
        self.sink_id = 2
        self.streams = [{'supply_temperature':10,'target_temperature':55,'fluid':'water','fluid_cp':10,'flowrate':10,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]},{'supply_temperature':10,'target_temperature':55,'fluid':'water','fluid_cp':10,'flowrate':10,'saturday_on':1
                         ,'sunday_on':1,'shutdown_periods':[],'daily_periods':[[10,18]]}]



# SINK -------------------------------------------------
# Industry
# user can create multiples industry streams for one industry by running the same code -> same sink id must be used
industry_data = Industry_Process()
industry_stream_test = industry(industry_data)

print(industry_stream_test.flowrate,industry_stream_test.hourly_generation)

# Office/Hotel/Residential Building
building_data = Building()
building_test = building(building_data)
print(building_test)


# Greenhouse
greenhouse_data = Greenhouse()
greenhouse_test = greenhouse(greenhouse_data)

print(greenhouse_test)


