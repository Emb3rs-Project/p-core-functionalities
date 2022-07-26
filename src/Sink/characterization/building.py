import math
from ...utilities.kb import KB
from ...General.Auxiliary_General.schedule_hour import schedule_hour
from ...General.Auxiliary_General.month_last_hour import month_last_hour
from ...General.Simple_User.adjust_capacity import adjust_capacity
from .Auxiliary.building_climate_api import building_climate_api
from .Auxiliary.wall_area import wall_area
from .Auxiliary.surface_outside_rad_heat_loss import surface_outside_rad_heat_loss
from .Auxiliary.ht_indoor_air import ht_indoor_air
from .Auxiliary.building_dhw import building_dhw
from .Auxiliary.explicit_computation_component_temperature import explicit_computation_component_temperature
from .Auxiliary.steady_state_vertical_inner_wall import steady_state_vertical_inner_wall
from .Auxiliary.steady_state_horizontal_faced_down import steady_state_horizontal_face_down
from .Auxiliary.steady_state_horizontal_faced_up import steady_state_horizontal_face_up
from .Auxiliary.steady_state_vertical_inner_glass import steady_state_vertical_inner_glass
from .Auxiliary.steady_state_exterior_wall import steady_state_exterior_wall
from .Auxiliary.info_time_step_climate_data import info_time_step_climate_data
from .Auxiliary.ht_radiation_vertical_surface import ht_radiation_vertical_surface
from .Auxiliary.ht_radiation_horizontal_surface import ht_radiation_horizontal_surface
from ...Error_Handling.error_building import error_building
from ...Error_Handling.runtime_error import ModuleRuntimeException

def building(in_var, kb : KB):
    """Building characterization

    Simulates heat an cooling consumptions over the year, according to building specifications
    and climate weather data

    Parameters
    ----------
    in_var : dict
        All necessary data to perform the building characterization data, with the following key:

        platform: dict
            Data obtained from the platform, with the following keys:

                - location : list
                    location [º]; [latitude,longitude]

                - number_floor: int
                    number of floors

                - width_floor: float
                    floor width [m]

                - length_floor: float
                    floor length	[m]

                - height_floor: float
                    floor height [m]

                - ratio_wall_N: float
                    ratio of the North wall area in total north facade area (wall + window) []

                - ratio_wall_S: float
                    ratio of the South wall area in total north facade area (wall + window) []

                - ratio_wall_E: float
                    ratio of the East wall area in total north facade area (wall + window) []

                - ratio_wall_W: float
                    ratio of the West wall area in total north facade area (wall + window) []

                - daily_periods: float
                    period of daily periods [h]

                - shutdown_periods: list
                    period of days stream is not available [day]

                - saturday_on: int
                    if available on saturdays - available (1); not available (0)

                - sunday_on: int
                    if available on sundays - available (1); not available (0)

                - building_orientation: str
                    building’s main facade orientation; "N","S","E" or "W"

                - space_heating_type: int
                    Space heating type;
                           1 = Conventional; heaters working fluid supply temperature of 75ºC,  heaters working fluid return temperature of 45ºC)
                           2 = Low temperature; heaters working fluid supply temperature of 50ºC,  heaters working fluid return temperature of 30ºC)
                           3 = Specify Temperatures - Advanced Properties; of supply_temperature_heat and target_temperature_heat

                - T_cool_on: float
                    Cooling setpoint temperature [ºC]

                - T_heat_on: float
                    Heating setpoint temperature [ºC]

                - T_off_min: float
                    Heating setback setpoint temperature [ºC]

                - T_off_max: float
                    Cooling setback setpoint temperature  [ºC]

                - ref_system_fuel_type_heating: str
                    Fuel type associated; e.g. "natural_gas","electricity","biomass","fuel_oil","none"

                - ref_system_fuel_price_heating: float, optional
                    Fuel Price. If not given, obtained from KB

                - ref_system_eff_equipment_heating: float, optional
                    Efficiency of the heating equipment

                - ref_system_fuel_type_cooling: str
                    Fuel type associated

                - ref_system_fuel_price_cooling: float, optional
                    Fuel Price. If not given, obtained from KB

                - ref_system_eff_equipment_cooling: float
                    OPTIONAL] COP of the cooling equipment

                - real_heating_monthly_capacity: dict, optional
                    Real monthly data - for each month of the year

                - real_heating_yearly_capacity: float, optional
                    Real yearly data - single value

                - real_cooling_monthly_capacity: dict, optional
                    Real monthly data - for each month of the year

                - real_cooling_yearly_capacity: float, optional
                    Real yearly data - single value

                - number_person_per_floor: int, optional
                    Persons per floor

                - supply_temperature_heat: float, optional
                    Heating System ReturnTemperature [ºC]

                - target_temperature_heat: float, optional
                    Heating System Supply Temperature [ºC]

                - supply_temperature_cool: float, optional
                    Cooling System Return Temperature [ºC]

                - target_temperature_cool: float, optional
                    Cooling System Supply Temperature [ºC]

                - tau_glass: float, optional
                    glass windows transmissivity []

                - u_wall: float, optional
                    walls' U value [W/m2.K]

                - u_roof: float, optional
                    roof U value [W/m2.K]

                - u_glass: float, optional
                    glass windows U value [W/m2.K]

                - u_floor: float, optional
                    floor U value [W/m2.K]

                - alpha_wall: float, optional
                    walls’ radiation absorption coefficient []

                - alpha_floor: float, optional
                    floor’s radiation absorption coefficient []

                - alpha_glass: float, optional
                    windows’ radiation absorption coefficient []

                - cp_floor: float, optional
                    floor specific heat capacitance [J/kg.K]

                - cp_roof: float, optional
                    roof specific heat capacitance [J/kg.K]

                - cp_wall: float, optional
                    wall specific heat capacitance [J/kg.K]

                - air_change_hour: float, optional
                    air changes per hour due to infiltrations [1/h]

                - renewal_air_per_person: float, optional
                    fresh air changer per person [m3/s per person]

                - vol_dhw_set: float, optional
                    Volume of daily water consumption [m3]

                - Q_gain_per_floor: float, optional
                    Internal Gains [W/m2]

                - emissivity_wall: float, optional
                    Walls's emissivity

                - emissivity_glass: float, optional
                    Glass Window's emissivity

    kb: dict
        Knowledge Base data

    Returns
    -------
    output : dict
        Streams data

            - streams : list
                List with dicts of all streams with the following keys:

                    - id : int
                        stream ID []

                    - name : str
                        Stream name []

                    - object_type : str
                        DEFAULT = "stream" []

                    - object_linked_id
                        None: DEFAULT=NONE, since no equipment/process is associated

                    - stream_type : str
                        Stream designation []; inflow, outflow, excess_heat

                    - supply_temperature : float
                        Stream's supply/initial temperature [ºC]

                    - target_temperature : float
                        Stream's target/final temperature [ºC]

                    - fluid : str
                        Stream fluid name

                    - flowrate : float
                        Stream mass flowrate[kg/h]

                    - schedule : list
                        Hourly values between 0 and 1, according to the capacity ration on that hour

                    - hourly_generation: list
                        Stream's hourly capacity [kWh]

                    - capacity : float
                        Stream's capacity [kW]

                    - monthly_generation : list
                        Stream's monthly capacity [kWh]

                    - fuel : str
                        Associated equipment fuel name []

                    - eff_equipment : float
                        Associated equipment efficiency []

    """

    ################################################################################################
    # INPUT ----------------------------------------------
    platform_data = error_building(in_var['platform'], kb)
    latitude, longitude = platform_data.location
    number_floor = platform_data.number_floor
    width_floor = platform_data.width_floor
    length_floor = platform_data.length_floor
    height_floor = platform_data.height_floor
    ratio_wall_N = platform_data.ratio_wall_N
    ratio_wall_S = platform_data.ratio_wall_S
    ratio_wall_E = platform_data.ratio_wall_E
    ratio_wall_W = platform_data.ratio_wall_W
    saturday_on = platform_data.saturday_on
    sunday_on = platform_data.sunday_on
    shutdown_periods = platform_data.shutdown_periods
    daily_periods = platform_data.daily_periods
    building_orientation = platform_data.building_orientation
    T_cool_on = platform_data.T_cool_on  # cooling start temperature working hours [ºC]
    T_heat_on = platform_data.T_heat_on  # heating start temperature working hours [ºC]
    T_off_min = platform_data.T_off_min  # heating start temperature off peak [ºC]
    T_off_max = platform_data.T_off_max  # cooling start temperature off peak [ºC
    number_person_per_floor = platform_data.number_person_per_floor # number of occupants per floor
    supply_temperature_heat = platform_data.supply_temperature_heat  # Heating
    target_temperature_heat = platform_data.target_temperature_heat
    supply_temperature_cool = platform_data.supply_temperature_cool  # Cooling
    target_temperature_cool = platform_data.target_temperature_cool
    tau_glass = platform_data.tau_glass  # Glass transmissivity
    u_wall = platform_data.u_wall  # Wall heat transfer coefficient [W/m2.K]
    u_roof = platform_data.u_roof
    u_glass = platform_data.u_glass
    u_floor = platform_data.u_floor
    alpha_wall = platform_data.alpha_wall
    alpha_floor = platform_data.alpha_floor
    alpha_glass = platform_data.alpha_glass
    cp_floor = platform_data.cp_floor  # Specific heat capacitance [J/m2.K]
    cp_roof = platform_data.cp_roof
    cp_wall = platform_data.cp_wall
    air_change_hour = platform_data.air_change_hour  # air changes per hour [1/h]
    renewal_air_per_person = platform_data.renewal_air_per_person  # [m3/s.person]
    vol_dhw_set = platform_data.vol_dhw_set
    Q_gain_per_floor = platform_data.Q_gain_per_floor
    emissivity_wall = platform_data.emissivity_wall
    emissivity_glass = platform_data.emissivity_glass

    ref_system_eff_equipment_heating = platform_data.ref_system_eff_equipment_heating
    ref_system_fuel_type_heating = platform_data.ref_system_fuel_type_heating
    ref_system_eff_equipment_cooling = platform_data.ref_system_eff_equipment_cooling
    ref_system_fuel_type_cooling = platform_data.ref_system_fuel_type_cooling

    real_heating_monthly_capacity = platform_data.real_heating_monthly_capacity
    real_heating_yearly_capacity = platform_data.real_heating_yearly_capacity
    real_cooling_monthly_capacity = platform_data.real_cooling_monthly_capacity
    real_cooling_yearly_capacity = platform_data.real_cooling_yearly_capacity


    ################################################################################################
    # DEFINED VARS ----------------------------------------------------------------------------------
    consumer_type = "household"
    # Simulation Properties
    interpolation_weight = 0.8

    # Building Properties
    T_ground = 15  # ground temperature [ºC]
    T_net = 15  # domestic water inlet temperature [ºC]
    T_dhw = 38  # domestic hot water (dhw) temperature [ºC]
    u_wall = 1 / (1 / u_wall - 0.13 - 0.04)
    u_glass = 1 / (1 / u_glass - 0.13 - 0.04)  # removed associated with outer/inner convection
    u_wall = u_wall * 2
    u_roof = 1 / (1 / u_roof - 0.13 - 0.04) * 2
    u_floor = 1 / (1 / u_floor - 0.13 - 0.04) * 2
    u_deck = u_roof
    alpha_roof = alpha_wall

    # Fluids/Material Properties
    rho_water = 997  # [kg/m3]
    cp_water = 4200  # [J/kg.K]
    rho_air = 1.225  # [kg/m3]
    cp_air = 1005  # [J/kg.K]


    ################################################################################################
    # COMPUTE ----------------------------------------------
    # Schedule
    profile = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)  # vector: [0,1,1,0,..]; 0-on 1-off
    month_last_hour_vector = month_last_hour()

    # Climate data
    try:
        df_climate = building_climate_api(latitude, longitude)
    except:
        raise ModuleRuntimeException(
            code="3",
            type="building.py",
            msg="Building characterization infeasible. Climate data not possible to obtain, change location or try later."
        )


    # Building Properties
    area_floor = width_floor * length_floor
    area_N_facade = wall_area('N', building_orientation, width_floor, length_floor, height_floor)  # area facade (wall+glass) [m2]
    area_S_facade = wall_area('S', building_orientation, width_floor, length_floor, height_floor)
    area_E_facade = wall_area('E', building_orientation, width_floor, length_floor, height_floor)
    area_W_facade = wall_area('W', building_orientation, width_floor, length_floor, height_floor)
    area_N_wall = area_N_facade * ratio_wall_N  # area North wall [m2]
    area_S_wall = area_S_facade * ratio_wall_S
    area_E_wall = area_E_facade * ratio_wall_E
    area_W_wall = area_W_facade * ratio_wall_W
    ratio_glass_in_N = (1 - ratio_wall_N)  # glass area fraction
    ratio_glass_in_S = (1 - ratio_wall_S)
    ratio_glass_in_E = (1 - ratio_wall_E)
    ratio_glass_in_W = (1 - ratio_wall_W)
    area_N_glass = area_N_facade * ratio_glass_in_N  # area North glass [m2]
    area_S_glass = area_S_facade * ratio_glass_in_S
    area_E_glass = area_E_facade * ratio_glass_in_E
    area_W_glass = area_W_facade * ratio_glass_in_W
    volume_floor = area_floor * height_floor  # indoor air volume per floor [m3]
    air_change_second = air_change_hour * volume_floor / 3600  # air infiltration im SI units [m3/s]
    c_roof = cp_roof * area_floor  # roof heat capacitance [J/K]
    c_floor = cp_floor * area_floor
    c_deck = cp_floor * area_floor
    c_N_wall = cp_wall * area_N_wall  # N wall heat capacitance [J/K]
    c_S_wall = cp_wall * area_S_wall
    c_E_wall = cp_wall * area_E_wall
    c_W_wall = cp_wall * area_W_wall


    # SIMULATION ----------------------------------------------
    # Initialize vars
    flowrate_dhw_set = 6 / 60000 * number_person_per_floor * 0.5  # combined DHW flowrate per floor [m3/s]
    profile_hourly_heat = []
    profile_hourly_cool = []
    profile_monthly_heat = []
    profile_monthly_cool = []
    T_interior = 15  # floor interior air temperature
    T_N_wall = 15  # wall temperature
    T_S_wall = 15
    T_E_wall = 15
    T_W_wall = 15
    T_N_wall_in = 15  # interior surface wall temperature
    T_S_wall_in = 15
    T_E_wall_in = 15
    T_W_wall_in = 15
    T_N_wall_out = 15  # exterior surface wall temperature
    T_S_wall_out = 15
    T_E_wall_out = 15
    T_W_wall_out = 15
    T_N_glass_out = 15
    T_S_glass_out = 15
    T_E_glass_out = 15
    T_W_glass_out = 15
    T_N_glass_in = 15
    T_E_glass_in = 15
    T_W_glass_in = 15
    T_S_glass_in = 15
    T_roof = 15  # last floor. roof temperature
    T_roof_in = 15
    T_roof_out = 15
    T_deck = 15  # deck temperature
    T_deck_above = 15  # floor of building floors (above zero floor)
    T_deck_below = 15  # deck of building floors larger than 0, except last floor
    T_floor = 15  # zero floor, floor temperature
    T_floor_in = 15
    vol_dhw = 0
    cumulative_heat_monthly = 0
    cumulative_cool_monthly = 0

    glass_in_N = {'type': 'glass', 'area': area_N_glass, 'temperature': T_N_glass_in}
    glass_in_E = {'type': 'glass', 'area': area_E_glass, 'temperature': T_E_glass_in}
    glass_in_S = {'type': 'glass', 'area': area_S_glass, 'temperature': T_S_glass_in}
    glass_in_W = {'type': 'glass', 'area': area_W_glass, 'temperature': T_W_glass_in}
    wall_in_N = {'type': 'wall', 'area': area_N_wall, 'temperature': T_N_wall_in}
    wall_in_E = {'type': 'wall', 'area': area_E_wall, 'temperature': T_E_wall_in}
    wall_in_S = {'type': 'wall', 'area': area_S_wall, 'temperature': T_S_wall_in}
    wall_in_W = {'type': 'wall', 'area': area_W_wall, 'temperature': T_W_wall_in}
    deck_below_in = {'type': 'wall', 'area': area_floor, 'temperature': T_deck_below}
    deck_above_in = {'type': 'wall', 'area': area_floor, 'temperature': T_deck_above}
    roof_in = {'type': 'wall', 'area': area_floor, 'temperature': T_roof_in}
    floor_in = {'type': 'wall', 'area': area_floor, 'temperature': T_floor_in}

    # Simulation Info
    time_step = 15*60  # time step [s]
    time_step_number_in_one_hour = int(3600 / time_step)  # time step number
    max_air_delta_T_per_minute = 1  # 1ºC per min
    max_air_delta_T_allowed = time_step * max_air_delta_T_per_minute / 60

    try:
        for profile_index, profile_operating in enumerate(profile):

            if (profile_index in month_last_hour_vector) or (profile_index == (len(profile) - 1)):
                profile_monthly_heat.append(round(cumulative_heat_monthly,2))  # space heating demand [kWh]
                profile_monthly_cool.append(round(cumulative_cool_monthly,2))  # space cooling demand [kWh]
                cumulative_heat_monthly = 0  # reset monthly heating needs
                cumulative_cool_monthly = 0  # reset monthly cooling needs

            cumulative_heat_hourly = 0  # reset hourly heating needs
            cumulative_cool_hourly = 0  # reset hourly cooling needs

            if profile_index == (len(profile) - 1):
                break

            for i in range(time_step_number_in_one_hour):

                # CLIMATE DATA --------------------------------------------------------------------------------------
                T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed = info_time_step_climate_data(
                    df_climate, profile_index, time_step_number_in_one_hour, i)

                # Correct wind speed
                z_0 = 0.01  # surface roughness
                wind_speed = wind_speed * (math.log((height_floor * number_floor / 2) / z_0)) / (
                    math.log(10 / z_0))  # correct wind speed of 10m for the average building height [m/s]
                u_exterior = (5.8 + 3.94 * wind_speed)  # outside heat convection coef. [W/m2.K]

                # BUILDING  --------------------------------------------------------------------------------------
                # Solar radiation floor
                Q_sun_floor = (Q_sun_N_facade * area_N_glass + Q_sun_S_facade * area_S_glass + Q_sun_E_facade * area_E_glass + Q_sun_W_facade * area_W_glass) * tau_glass  # total transmitted radiation by glass to floor/deck [W]

                # Radiation Heat Transfer
                Q_rad_N_glass = ht_radiation_vertical_surface(glass_in_N, glass_in_E, glass_in_S, glass_in_W, wall_in_E,
                                                              wall_in_S, wall_in_W, deck_below_in, deck_above_in,
                                                              emissivity_wall, emissivity_glass)  # North Glass
                Q_rad_N_wall = ht_radiation_vertical_surface(wall_in_N, glass_in_E, glass_in_S, glass_in_W, wall_in_E,
                                                             wall_in_S, wall_in_W, deck_below_in, deck_above_in,
                                                             emissivity_wall, emissivity_glass)  # North Wall
                Q_rad_E_glass = ht_radiation_vertical_surface(glass_in_E, glass_in_N, glass_in_S, glass_in_W, wall_in_N,
                                                              wall_in_S, wall_in_W, deck_below_in, deck_above_in,
                                                              emissivity_wall, emissivity_glass)
                Q_rad_E_wall = ht_radiation_vertical_surface(wall_in_E, glass_in_N, glass_in_S, glass_in_W, wall_in_N,
                                                             wall_in_S, wall_in_W, deck_below_in, deck_above_in,
                                                             emissivity_wall, emissivity_glass)
                Q_rad_S_glass = ht_radiation_vertical_surface(glass_in_S, glass_in_E, glass_in_N, glass_in_W, wall_in_E,
                                                              wall_in_N, wall_in_W, deck_below_in, deck_above_in,
                                                              emissivity_wall, emissivity_glass)
                Q_rad_S_wall = ht_radiation_vertical_surface(wall_in_S, glass_in_E, glass_in_N, glass_in_W, wall_in_E,
                                                             wall_in_N, wall_in_W, deck_below_in, deck_above_in,
                                                             emissivity_wall, emissivity_glass)
                Q_rad_W_glass = ht_radiation_vertical_surface(glass_in_W, glass_in_E, glass_in_S, glass_in_N, wall_in_E,
                                                              wall_in_S, wall_in_N, deck_below_in, deck_above_in,
                                                              emissivity_wall, emissivity_glass)
                Q_rad_W_wall = ht_radiation_vertical_surface(wall_in_W, glass_in_E, glass_in_S, glass_in_N, wall_in_E,
                                                             wall_in_S, wall_in_N, deck_below_in, deck_above_in,
                                                             emissivity_wall, emissivity_glass)
                Q_rad_deck_below = ht_radiation_horizontal_surface(deck_below_in, wall_in_W, glass_in_W, glass_in_E,
                                                                   glass_in_S, glass_in_N, wall_in_E, wall_in_S, wall_in_N,
                                                                   deck_above_in, emissivity_wall, emissivity_glass)
                Q_rad_deck_above = ht_radiation_horizontal_surface(deck_above_in, wall_in_W, glass_in_W, glass_in_E,
                                                                   glass_in_S, glass_in_N, wall_in_E, wall_in_S, wall_in_N,
                                                                   deck_below_in, emissivity_wall, emissivity_glass)
                Q_rad_roof = ht_radiation_horizontal_surface(roof_in, wall_in_W, glass_in_W, glass_in_E, glass_in_S,
                                                             glass_in_N, wall_in_E, wall_in_S, wall_in_N, deck_above_in,
                                                             emissivity_wall, emissivity_glass)
                Q_rad_floor = ht_radiation_horizontal_surface(floor_in, wall_in_W, glass_in_W, glass_in_E, glass_in_S,
                                                              glass_in_N, wall_in_E, wall_in_S, wall_in_N, deck_below_in,
                                                              emissivity_wall, emissivity_glass)

                # Sky Radiation Heat Losses
                Q_infra_N_outer_wall = surface_outside_rad_heat_loss(emissivity_wall, T_N_wall_out, T_sky, T_exterior,
                                                                     math.pi / 2)  # Radiation heat loss [W/m2]
                Q_infra_S_outer_wall = surface_outside_rad_heat_loss(emissivity_wall, T_S_wall_out, T_sky, T_exterior,
                                                                     math.pi / 2)
                Q_infra_E_outer_wall = surface_outside_rad_heat_loss(emissivity_wall, T_E_wall_out, T_sky, T_exterior,
                                                                     math.pi / 2)
                Q_infra_W_outer_wall = surface_outside_rad_heat_loss(emissivity_wall, T_W_wall_out, T_sky, T_exterior,
                                                                     math.pi / 2)
                Q_infra_N_outer_glass = surface_outside_rad_heat_loss(emissivity_glass, T_N_glass_out, T_sky, T_exterior,
                                                                      math.pi / 2)
                Q_infra_S_outer_glass = surface_outside_rad_heat_loss(emissivity_glass, T_S_glass_out, T_sky, T_exterior,
                                                                      math.pi / 2)
                Q_infra_E_outer_glass = surface_outside_rad_heat_loss(emissivity_glass, T_E_glass_out, T_sky, T_exterior,
                                                                      math.pi / 2)
                Q_infra_W_outer_glass = surface_outside_rad_heat_loss(emissivity_glass, T_W_glass_out, T_sky, T_exterior,
                                                                      math.pi / 2)
                Q_infra_roof_out = surface_outside_rad_heat_loss(emissivity_wall, T_roof_out, T_sky, T_exterior, 0)

                # Each floor Heat balance of indoor temperature [W]
                surfaces_vertical = [glass_in_N, glass_in_E, glass_in_S, glass_in_W, wall_in_E, wall_in_S, wall_in_W,
                                     wall_in_N]
                if number_floor > 1:
                    surfaces_horizontal = [roof_in, deck_above_in]
                    top_floor = ht_indoor_air(T_interior, surfaces_horizontal, surfaces_vertical)
                    surfaces_horizontal = [deck_above_in, deck_below_in]
                    middle_floor = ht_indoor_air(T_interior, surfaces_horizontal, surfaces_vertical)
                    surfaces_horizontal = [deck_below_in, floor_in]
                    bottom_floor = ht_indoor_air(T_interior, surfaces_horizontal, surfaces_vertical)
                else:
                    surfaces_horizontal = [roof_in, floor_in]
                    zero_floor = ht_indoor_air(T_interior, surfaces_horizontal, surfaces_vertical)

                # Average floor Heat balance before space heating/cooling
                if number_floor == 1:
                    Q_building_floor = (rho_air * cp_air * renewal_air_per_person * number_person_per_floor) * (
                            T_exterior - T_interior) * profile_operating \
                                       + rho_air * cp_air * air_change_second * (T_exterior - T_interior) \
                                       + Q_gain_per_floor * profile_operating \
                                       + zero_floor  # [W]
                else:
                    Q_building_floor = (rho_air * cp_air * renewal_air_per_person * number_person_per_floor) * (
                            T_exterior - T_interior) * profile_operating \
                                       + rho_air * cp_air * air_change_second * (T_exterior - T_interior) \
                                       + Q_gain_per_floor * profile_operating \
                                       + (top_floor + middle_floor * (number_floor - 2) + bottom_floor) / number_floor

                # SPACE HEATING/COOLING ACTUATION --------------------------------------------------------
                # off work time
                if profile_operating == 0:
                    T_interior_guess = T_interior + (Q_building_floor) * time_step / (
                            rho_air * cp_air * volume_floor)  # [ºC]

                    # outside temperature interval - activating space heating
                    if T_interior < T_off_min and T_interior_guess < T_off_min:
                        if Q_building_floor < 0:
                            if T_off_min - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = abs(Q_building_floor) + (rho_air * cp_air * volume_floor) * (
                                        T_off_min - T_interior) / time_step  # [W]
                            else:
                                Q_heat_required = abs(Q_building_floor) + (
                                        rho_air * cp_air * volume_floor) * max_air_delta_T_allowed / time_step
                        else:
                            if T_interior_guess - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = (rho_air * cp_air * volume_floor) * (
                                        max_air_delta_T_allowed - (T_interior_guess - T_interior)) / time_step
                            else:
                                Q_heat_required = 0

                    # inside temperature interval - activating space heating
                    elif T_interior >= T_off_min and T_interior_guess < T_off_min:
                        Q_heat_required = (rho_air * cp_air * volume_floor) * (T_off_min - T_interior_guess) / time_step

                    # inside temperature interval - activating space cooling
                    elif T_interior <= T_off_max and T_interior_guess > T_off_max:  # above temperature range
                        Q_heat_required = (rho_air * cp_air * volume_floor) * (T_off_max - T_interior_guess) / time_step

                    # outside temperature interval - activating space cooling
                    elif T_interior > T_off_max and T_interior_guess > T_off_max:
                        if Q_building_floor > 0:
                            if T_interior - T_off_max < max_air_delta_T_allowed:
                                Q_heat_required = -Q_building_floor - (rho_air * cp_air * volume_floor) * (
                                        max_air_delta_T_allowed - (T_interior - T_off_max)) / time_step
                            else:
                                Q_heat_required = -Q_building_floor - (rho_air * cp_air * volume_floor) * (
                                    max_air_delta_T_allowed) / time_step
                        else:
                            if T_interior - T_interior_guess < max_air_delta_T_allowed:
                                Q_heat_required = - (rho_air * cp_air * volume_floor) * (
                                        max_air_delta_T_allowed - (T_interior - T_interior_guess)) / time_step
                            else:
                                Q_heat_required = 0
                    else:
                        Q_heat_required = 0

                # on work time
                else:
                    T_interior_guess = T_interior + (Q_building_floor) * time_step / (rho_air * cp_air * volume_floor)

                    # activating space heating
                    if T_interior < T_heat_on and T_interior_guess < T_heat_on:
                        if Q_building_floor < 0:
                            if T_heat_on - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = abs(Q_building_floor) + (rho_air * cp_air * volume_floor) * (
                                        T_heat_on - T_interior) / time_step
                            else:
                                Q_heat_required = abs(Q_building_floor) + (
                                        rho_air * cp_air * volume_floor) * max_air_delta_T_allowed / time_step
                        else:
                            if T_interior_guess - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = (rho_air * cp_air * volume_floor) * (
                                        max_air_delta_T_allowed - (T_interior_guess - T_interior)) / time_step
                            else:
                                Q_heat_required = 0

                    # activating space heating
                    elif T_interior >= T_heat_on and T_interior_guess < T_heat_on:
                        Q_heat_required = (rho_air * cp_air * volume_floor) * (T_heat_on - T_interior_guess) / time_step

                    # activating space cooling
                    elif T_interior <= T_cool_on and T_interior_guess > T_cool_on:  # above temperature range
                        Q_heat_required = (rho_air * cp_air * volume_floor) * (T_cool_on - T_interior_guess) / time_step

                    elif T_interior == T_cool_on and T_interior_guess >= T_cool_on:  # above temperature range
                        Q_heat_required = -Q_building_floor

                    # activating space cooling
                    elif T_interior > T_cool_on and T_interior_guess > T_cool_on:
                        if Q_building_floor > 0:
                            if T_interior - T_cool_on < max_air_delta_T_allowed:
                                Q_heat_required = -Q_building_floor - (rho_air * cp_air * volume_floor) * (
                                        T_interior - T_cool_on) / time_step
                            else:
                                Q_heat_required = -Q_building_floor - (rho_air * cp_air * volume_floor) * (
                                    max_air_delta_T_allowed) / time_step
                        else:
                            if T_interior - T_interior_guess < max_air_delta_T_allowed:
                                Q_heat_required = - (rho_air * cp_air * volume_floor) * (
                                        max_air_delta_T_allowed - (T_interior - T_interior_guess)) / time_step
                            else:
                                Q_heat_required = 0
                    else:
                        Q_heat_required = 0

                # HOT WATER CONSUMPTION -------------------------------------------------------------------------
                flowrate_dhw, vol_dhw = building_dhw(profile_index, vol_dhw_set, vol_dhw, flowrate_dhw_set,
                                                     time_step)  # [m3/s]; [m3]
                Q_dwh = rho_water * cp_water * flowrate_dhw * (T_dhw - T_net)  # [W]

                # COMPUTE TEMPERATURES  -------------------------------------------------------------------------
                # Steady State Heat Balances
                # Inner Surfaces
                T_deck_above = steady_state_horizontal_face_up(Q_sun_floor, T_deck_above, T_deck, T_interior, u_deck,
                                                               Q_rad_deck_above, area_floor, alpha_floor,
                                                               interpolation_weight)
                T_deck_below = steady_state_horizontal_face_down(T_deck_below, T_deck, T_interior, u_deck, Q_rad_deck_below,
                                                                 area_floor, interpolation_weight)
                T_N_wall_in = steady_state_vertical_inner_wall(T_N_wall_in, T_N_wall, T_interior, u_wall, Q_rad_N_wall,
                                                               area_N_wall, interpolation_weight)
                T_S_wall_in = steady_state_vertical_inner_wall(T_S_wall_in, T_S_wall, T_interior, u_wall, Q_rad_S_wall,
                                                               area_S_wall, interpolation_weight)
                T_E_wall_in = steady_state_vertical_inner_wall(T_E_wall_in, T_E_wall, T_interior, u_wall, Q_rad_E_wall,
                                                               area_E_wall, interpolation_weight)
                T_W_wall_in = steady_state_vertical_inner_wall(T_W_wall_in, T_W_wall, T_interior, u_wall, Q_rad_W_wall,
                                                               area_W_wall, interpolation_weight)
                T_N_glass_in = steady_state_vertical_inner_glass(Q_sun_N_facade, alpha_glass, T_N_glass_in, T_N_glass_out,
                                                                 T_interior, u_glass, Q_rad_N_glass, area_N_glass,
                                                                 interpolation_weight)
                T_S_glass_in = steady_state_vertical_inner_glass(Q_sun_S_facade, alpha_glass, T_S_glass_in, T_S_glass_out,
                                                                 T_interior, u_glass, Q_rad_S_glass, area_S_glass,
                                                                 interpolation_weight)

                T_E_glass_in = steady_state_vertical_inner_glass(Q_sun_E_facade, alpha_glass, T_E_glass_in, T_E_glass_out,
                                                                 T_interior, u_glass, Q_rad_E_glass, area_E_glass,
                                                                 interpolation_weight)
                T_W_glass_in = steady_state_vertical_inner_glass(Q_sun_W_facade, alpha_glass, T_W_glass_in, T_W_glass_out,
                                                                 T_interior, u_glass, Q_rad_W_glass, area_W_glass,
                                                                 interpolation_weight)
                T_roof_in = steady_state_horizontal_face_down(T_roof_in, T_roof, T_interior, u_roof, Q_rad_roof, area_floor,
                                                              interpolation_weight)
                T_floor_in = steady_state_horizontal_face_up(Q_sun_floor, T_floor_in, T_floor, T_interior, u_floor,
                                                             Q_rad_floor, area_floor, alpha_floor, interpolation_weight)

                # Outer Surfaces
                T_roof_out = steady_state_exterior_wall(T_roof_out, T_roof, T_exterior, u_wall, Q_sun_roof,
                                                        Q_infra_roof_out, alpha_roof, u_exterior, interpolation_weight)
                T_N_wall_out = steady_state_exterior_wall(T_N_wall_out, T_N_wall, T_exterior, u_wall, Q_sun_N_facade,
                                                          Q_infra_N_outer_wall, alpha_wall, u_exterior,
                                                          interpolation_weight)
                T_S_wall_out = steady_state_exterior_wall(T_S_wall_out, T_S_wall, T_exterior, u_wall, Q_sun_S_facade,
                                                          Q_infra_S_outer_wall, alpha_wall, u_exterior,
                                                          interpolation_weight)
                T_E_wall_out = steady_state_exterior_wall(T_E_wall_out, T_E_wall, T_exterior, u_wall, Q_sun_E_facade,
                                                          Q_infra_E_outer_wall, alpha_wall, u_exterior,
                                                          interpolation_weight)
                T_W_wall_out = steady_state_exterior_wall(T_W_wall_out, T_W_wall, T_exterior, u_wall, Q_sun_W_facade,
                                                          Q_infra_W_outer_wall, alpha_wall, u_exterior,
                                                          interpolation_weight)
                T_N_glass_out = steady_state_exterior_wall(T_N_glass_out, T_N_glass_in, T_exterior, u_glass, Q_sun_N_facade,
                                                           Q_infra_N_outer_glass, alpha_glass, u_exterior,
                                                           interpolation_weight)
                T_S_glass_out = steady_state_exterior_wall(T_S_glass_out, T_S_glass_in, T_exterior, u_glass, Q_sun_S_facade,
                                                           Q_infra_S_outer_glass, alpha_glass, u_exterior,
                                                           interpolation_weight)
                T_E_glass_out = steady_state_exterior_wall(T_E_glass_out, T_E_glass_in, T_exterior, u_glass, Q_sun_E_facade,
                                                           Q_infra_E_outer_glass, alpha_glass, u_exterior,
                                                           interpolation_weight)
                T_W_glass_out = steady_state_exterior_wall(T_W_glass_out, T_W_glass_in, T_exterior, u_glass, Q_sun_W_facade,
                                                           Q_infra_W_outer_glass, alpha_glass, u_exterior,
                                                           interpolation_weight)

                # Explicit Heat Balances
                # Interior Air
                T_interior = T_interior + (Q_building_floor + Q_heat_required) * time_step / (
                        rho_air * cp_air * volume_floor)  # [ºC]

                # Wall
                T_N_wall = explicit_computation_component_temperature(T_N_wall, T_N_wall_in, T_N_wall_out, u_wall,
                                                                      area_N_wall, time_step, c_N_wall)
                T_S_wall = explicit_computation_component_temperature(T_S_wall, T_S_wall_in, T_S_wall_out, u_wall,
                                                                      area_S_wall, time_step, c_S_wall)
                T_E_wall = explicit_computation_component_temperature(T_E_wall, T_E_wall_in, T_E_wall_out, u_wall,
                                                                      area_E_wall, time_step, c_E_wall)
                T_W_wall = explicit_computation_component_temperature(T_W_wall, T_W_wall_in, T_W_wall_out, u_wall,
                                                                      area_W_wall, time_step, c_W_wall)
                T_roof = explicit_computation_component_temperature(T_roof, T_roof_in, T_roof_out, u_roof, area_floor,
                                                                    time_step, c_roof)
                T_floor = explicit_computation_component_temperature(T_floor, T_floor_in, T_ground, u_floor, area_floor,
                                                                     time_step, c_floor)
                T_deck = explicit_computation_component_temperature(T_deck, T_deck_above, T_deck_below, u_deck, area_floor,
                                                                    time_step, c_deck)

                # Generate Profiles Data
                if Q_heat_required > 0:
                    cumulative_heat_monthly += (Q_heat_required + Q_dwh) * time_step / 3600000  # [kWh]
                    cumulative_heat_hourly += (Q_heat_required + Q_dwh) * time_step / 3600000

                else:
                    cumulative_cool_monthly += (abs(Q_heat_required) * time_step / 3600000)
                    cumulative_cool_hourly += (abs(Q_heat_required) * time_step / 3600000)

                # Update Info
                glass_in_N['temperature'] = T_N_glass_in
                glass_in_E['temperature'] = T_E_glass_in
                glass_in_S['temperature'] = T_S_glass_in
                glass_in_W['temperature'] = T_W_glass_in
                wall_in_N['temperature'] = T_N_wall_in
                wall_in_E['temperature'] = T_E_wall_in
                wall_in_S['temperature'] = T_S_wall_in
                wall_in_W['temperature'] = T_W_wall_in
                deck_below_in['temperature'] = T_deck_below
                deck_above_in['temperature'] = T_deck_above
                roof_in['temperature'] = T_roof_in
                floor_in['temperature'] = T_floor_in

            # Hourly Profiles
            profile_hourly_heat.append(cumulative_heat_hourly)  # hourly space heating demand [kWh]
            profile_hourly_cool.append(cumulative_cool_hourly)  # hourly space cooling demand [kWh]

        profile_monthly_heat = [i * number_floor for i in profile_monthly_heat]
        profile_monthly_cool = [i * number_floor for i in profile_monthly_cool]
        profile_hourly_heat = [i * number_floor for i in profile_hourly_heat]
        profile_hourly_cool = [i * number_floor for i in profile_hourly_cool]

        # Adjust Capacity
        stream_hot = {
                'id': 1,
                'name': "building heating",
                'object_type': 'stream',
                'fluid': 'water',
                'stream_type': 'inflow',
                'capacity': max(profile_hourly_heat),
                "monthly_generation": profile_monthly_heat,  # [kWh]
                "hourly_generation": profile_hourly_heat,  # [kWh]
                "supply_temperature": supply_temperature_heat,  # [ºC]
                "target_temperature": target_temperature_heat,  # [ºC]
                "schedule": profile,
                "fuel": ref_system_fuel_type_heating,
                "eff_equipment": ref_system_eff_equipment_heating
        }


        stream_cold = {
                'id': 2,
                'name': "building cooling",
                'object_type': 'stream',
                'fluid': 'water',
                'stream_type': 'inflow',
                'capacity': max(profile_hourly_cool),
                "monthly_generation": profile_monthly_cool,  # [kWh]
                "hourly_generation": profile_hourly_cool,  # [kWh]
                "supply_temperature": supply_temperature_cool,  # [ºC]
                "target_temperature": target_temperature_cool,  # [ºC]
                "schedule": profile,
                "fuel": ref_system_fuel_type_cooling,
                "eff_equipment": ref_system_eff_equipment_cooling
            }

        if real_heating_monthly_capacity is not None:
            stream_hot = adjust_capacity(stream_hot, user_monthly_capacity=vars(real_heating_monthly_capacity))
        elif real_heating_yearly_capacity is not None:
            stream_hot = adjust_capacity(stream_hot, user_yearly_capacity=real_heating_yearly_capacity)

        if real_cooling_monthly_capacity is not None:
            stream_cold = adjust_capacity(stream_cold, user_monthly_capacity=vars(real_cooling_monthly_capacity))
        elif real_cooling_yearly_capacity is not None:
            stream_cold = adjust_capacity(stream_cold, user_yearly_capacity=real_cooling_yearly_capacity)


        ##############################
        # OUTPUT
        output = {'streams': [stream_hot, stream_cold]}


    except:
        raise ModuleRuntimeException(
            code="1",
            type="building.py",
            msg="Building characterization infeasible. Please check your inputs."
        )


    return output



