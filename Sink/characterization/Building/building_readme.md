The building function generates the building yearly space heating and cooling demand from the user input data.
It reads the user input data from the platform frontdend namely:
**Mandatory/Basic User inputs:**
1. latitude
1. longitude
1. number_floor
1. width_floor [m]
1. length_floor [m]
1. height_floor [m]
1. ratio_wall_N 1. value between  0 and 1
1. ratio_wall_S
1. ratio_wall_E
1. ratio_wall_W
1. saturday_on 1. 1 (yes)  or 0 (no)
1. sunday_on 1. 1 (yes)  or 0 (no)
1. shutdown_periods 1. array with day arrays e.g. [[130,140],[289,299]]
1. daily_periods 1. array with hour arrays; e.g. [[8,12],[15,19]]
1. building_type 1. 'office','residential' or ' hotel'
1. building_orientation 1. 'N','S','E' or 'W'

**IMPORTANT:**
1. if  building_type = 'residential' -> mandatory input -> number_person_per_floor
1. if  building_type = 'hotel' -> mandatory input -> number_rooms
1. space_heating_type -> mandatory input for basic user 1. Expert User should introduce temperatures
    - 0 = Conventional (target_temperature_heat = 75; supply_temperature_heat = 45)
    - 1 = Low temperature (target_temperature_heat = 50; supply_temperature_heat = 30)

**Optional/Expert User inputs:**
1. number_person_per_floor
1. supply_temperature_heat [ºC]
1. target_temperature_heat [ºC]
1. supply_temperature_cool [ºC]
1. target_temperature_cool [ºC]
1. T_cool_on [ºC]
1. T_heat_on [ºC]
1. T_off_min [ºC]
1. T_off_max [ºC]
1. tau_glass 1. value between  0 and 1
1. alpha_wall
1. alpha_floor
1. alpha_glass
1. u_wall [W/m2.K]
1. u_roof
1. u_floor
1. u_glass
1. cp_roof [J/m2.K]
1. cp_wall [J/m2.K]
1. air_change_hour [1/h]
1. renewal_air_per_person  [m3/s.person]
1. vol_dhw_set 1. daily water consumption [m3]
1. Q_gain_per_floor


**Function OUTPUT:** json with 2 dictionaries, regarding the building´s heating and cooling needs in a stream with:
1. id 1. stream id
1. object_type 1. stream
1. fluid 1. water
1. stream_type 1. inflow
1. monthly_generation 1. array [kWh]
1. hourly_generation 1. array [kWh]
1. supply_temperature [ºC]
1. target_temperature [ºC]

