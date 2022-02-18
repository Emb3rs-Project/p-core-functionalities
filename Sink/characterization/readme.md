# Sink characterization submodule

This submodule comprises the sink characterization of the the EMB3RS platform.

## Characterization of user-defined sinks (industrial)

There is one function to characterize industrial sinks or user-defined streams, the simplified_user function.

### simplified_user function

The function reads user input data and computes the related stream in json format.

#### INPUT
1. object_id = uuid (created automatically in the platform)
1. type_of_object = sink/source
1. streams = vector with dictionaries
1. supply_temperature = stream supply temperature (ºC)
1. target_temperature = stream target temperature (ºC)
1. fluid = stream fluid (list)
1. fluid_cp = specific heat capacity (kJ/kg.K)
1. flowrate = stream flowrate (kg/h)
1. saturday_on 1. 1 (yes)  or 0 (no)
1. sunday_on 1. 1 (yes)  or 0 (no)
1. shutdown_periods 1. array with day arrays e.g. [[130,140],[289,299]]
1. daily_periods 1. array with hour arrays; e.g. [[8,12],[15,19]]

#### OUTPUT
1. stream_id = uuid
1. object_type = stream
1. fluid = stream fluid (list)
1. schedule = Array with stream operating -1- or not -0- each hour
1. hourly_generation = Array with stream capacity available hourly
1. capacity = stream capacity in kW
1. supply_temperature (ºC)
1. target_temperature (ºC)


## Sink Characterization (Buildings)

In this submodule there are 2 main functions to characterize buildings, the buiilding function and the greenhouse function.

### Building function

The building function generates the building yearly space heating and cooling demand from the user input data. It has 3 main types of buildings (residential, hotel and office).
It reads the user input data from the platform frontdend namely:

#### Mandatory/Basic User inputs:
1. latitude
1. longitude
1. number_floor
1. width_floor [m]
1. length_floor [m]
1. height_floor [m]
1. saturday_on 1. 1 (yes)  or 0 (no)
1. sunday_on 1. 1 (yes)  or 0 (no)
1. shutdown_periods 1. array with day arrays e.g. [[130,140],[289,299]]
1. daily_periods 1. array with hour arrays; e.g. [[8,12],[15,19]]
1. building_type 1. 'office','residential' or ' hotel'
1. building_orientation 1. 'N','S','E' or 'W'

#### IMPORTANT inputs:
1. if  building_type = 'residential' -> mandatory input -> number_person_per_floor
1. if  building_type = 'hotel' -> mandatory input -> number_rooms
1. space_heating_type -> mandatory input for basic user 1. Expert User should introduce temperatures
    - 0 = Conventional (target_temperature_heat = 75; supply_temperature_heat = 45)
    - 1 = Low temperature (target_temperature_heat = 50; supply_temperature_heat = 30)

#### Optional inputs:
1. number_person_per_floor = number of occupants per floor
1. supply_temperature_heat = heating system supply temperature [ºC]
1. target_temperature_heat = heating system target temperature [ºC] 
1. supply_temperature_cool = cooling system supply temperature [ºC]
1. target_temperature_cool = cooling system target temperature [ºC]
1. T_cool_on [ºC]
1. T_heat_on [ºC]
1. T_off_min [ºC]
1. T_off_max [ºC]
1. tau_glass = shortwave transmission (value between  0 and 1)
1. alpha_wall = wall shortwave absorption coefficient (value between  0 and 1)
1. alpha_floor = floor/roof shortwave absorption coefficient (value between  0 and 1)
1. alpha_glass = glass shortwave absorption coefficient (value between  0 and 1)
1. u_wall = wall u-value to ambient air (W/m2.K)
1. u_roof = roof u-value to ambient air (W/m2.K)
1. u_floor = wall u-value to ambient air (W/m2.K)
1. u_glass = wall u-value to ambient air (W/m2.K)
1. air_change_hour = building air inflitration (/h)
1. renewal_air_per_person  = fresh air renewal per person [m3/s.person]
1. vol_dhw_set = daily water consumption [m3]
1. Q_gain_per_floor = indoor appliances heat gain (W/m2)

#### Function OUTPUT: json with 2 dictionaries, regarding the building´s heating and cooling needs in a stream with:
1. id 1. stream id
1. object_type 1. stream
1. fluid 1. water
1. stream_type 1. inflow
1. monthly_generation 1. array [kWh]
1. hourly_generation 1. array [kWh]
1. supply_temperature [ºC]
1. target_temperature [ºC]

### Greenhouse function

It simulates the yearly heating demand of a greenhouse depending on the climate data for the location.

#### Mandatory/Basic User inputs:
1. latitude
1. longitude
1. width_floor
1. length_floor
1. height_floor
1. shutdown_periods
1. daily_periods
1. building_orientation
1. saturday_on
1. sunday_on
1. lights_on - 1=with lights system ; 0=no lights system
1. hours_lights_needed - lighting hours in greenhouse (counting with daily iluminance) [h]

#### IMPORTANT - for Mandatory/Basic User:
1.  get  building_efficiency to compute f_c
- 1=tight sealed greenhouse
- 2=medium
- 3=loose

#### Optional/Expert User inputs:
1. f_c
1. T_cool_on = in_var.T_cool_on  [ºC]
1. T_heat_on = in_var.T_heat_on  [ºC]
1. supply_temperature_heat [ºC]
1. target_temperature_heat [ºC]
1. leaf_area_index - ratio of area_plants/area_floor, 0 to 1
1. rh_air - controlled interior air RH , 0 to 1
1. u_cover [W/m2.K]
1. indoor_air_speed [m/s]
1. leaf_length - characteristic leaf length [m]
1. tau_cover_long_wave_radiation - 0 to 1
1. emissivity_cover_long_wave_radiation - 0 to 1
1. tau_cover_solar_radiation - 0 to 1
1. power_lights [W/m2]

#### OUTPUT: json with 2 dictionaries, regarding hot and cooling stream needs with:
1. id - stream id
1. object_type - stream
1. fluid - water
1. stream_type - inflow
1. monthly_generation - array [kWh]
1. hourly_generation - array [kWh]
1. supply_temperature [ºC]
1. target_temperature [ºC]
