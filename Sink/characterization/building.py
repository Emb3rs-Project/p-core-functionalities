"""
alisboa/jmcunha


##############################
INFO: Building Simulation. Simulates heat an cooling consumptions over the year, according to building specifications
    and climate weather data


##############################
INPUT: dictionary with:

        Mandatory/Basic User inputs:
            # latitude  [º]
            # longitude  [º]
            # number_floor  []
            # width_floor [m]
            # length_floor [m]
            # height_floor [m]
            # ratio_wall_N - value between  0 and 1  []
            # ratio_wall_S
            # ratio_wall_E
            # ratio_wall_W
            # saturday_on - 1 (yes)  or 0 (no)
            # sunday_on - 1 (yes)  or 0 (no)
            # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
            # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]
            # building_type - 'office','residential' or ' hotel'
            # building_orientation - 'N','S','E' or 'W'

            !!!
            IMPORTANT -  for Mandatory/Basic User:
                # if  building_type = 'residential' -> mandatory input -> number_person_per_floor
                # if  building_type = 'hotel' -> mandatory input -> number_rooms
                # space_heating_type -> mandatory input for basic user - Expert User should introduce temperatures
                    -> 0 = Conventional (target_temperature_heat = 75; supply_temperature_heat = 45)
                    -> 1 = Low temperature (target_temperature_heat = 50; supply_temperature_heat = 30)

        Optional/Expert User inputs:
            # number_person_per_floor
            # supply_temperature_heat [ºC]
            # target_temperature_heat [ºC]
            # supply_temperature_cool [ºC]
            # target_temperature_cool [ºC]
            # T_cool_on [ºC]
            # T_heat_on [ºC]
            # T_off_min [ºC]
            # T_off_max [ºC]
            # tau_glass - value between  0 and 1  []
            # alpha_wall
            # alpha_floor
            # alpha_glass
            # u_wall [W/m2.K]
            # u_roof
            # u_floor
            # u_glass
            # cp_roof [J/m2.K]
            # cp_wall [J/m2.K]
            # air_change_hour [1/h]
            # renewal_air_per_person  [m3/s.person]
            # vol_dhw_set - daily water consumption [m3]
            # Q_gain_per_floor  [W]
            # emissivity_wall  []
            # emissivity_glass

##############################
OUTPUT: dict with key 'streams' with streams dictionaries - 'hot_stream' and 'cold_stream'

        Where for example:
        # 'hot_stream' = {
        #           'id' - stream id
        #           'object_type' - stream
        #           'fluid' - water
        #           'stream_type' - inflow
        #           'monthly_generation' - array [kWh]
        #           'hourly_generation' - array [kWh]
        #           'supply_temperature' [ºC]
        #           'target_temperature' [ºC]
        #           }


"""

import math
from ...utilities.kb import KB
from .Auxiliary.building_climate_api import building_climate_api
from .Auxiliary.wall_area import wall_area
from ...General.Auxiliary_General.schedule_hour import schedule_hour
from .Auxiliary.surface_outside_rad_heat_loss import surface_outside_rad_heat_loss
from .Auxiliary.ht_indoor_air import ht_indoor_air
from .Auxiliary.building_dhw import building_dhw
from ...General.Auxiliary_General.month_last_hour import month_last_hour
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

    ################################################################################################
    # DEFINED VARS ----------------------------------------------------------------------------------
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
    one_hour = int(3600 / time_step)  # time step number
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

            for i in range(one_hour):

                # CLIMATE DATA --------------------------------------------------------------------------------------
                T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed = info_time_step_climate_data(
                    df_climate, profile_index, one_hour, i)

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

        ##############################
        # OUTPUT
        streams = {
            'hot_stream': {
                'id': 1,
                'object_type': 'stream',
                'fluid': 'water',
                'stream_type': 'inflow',
                'capacity': max(profile_hourly_heat),
                "monthly_generation": profile_monthly_heat,  # [kWh]
                "hourly_generation": profile_hourly_heat,  # [kWh]
                "supply_temperature": supply_temperature_heat,  # [ºC]
                "target_temperature": target_temperature_heat,  # [ºC]
                "schedule": profile
            },
            'cold_stream': {
                'id': 2,
                'object_type': 'stream',
                'fluid': 'water',
                'stream_type': 'inflow',
                'capacity': max(profile_hourly_cool),
                "monthly_generation": profile_monthly_cool,  # [kWh]
                "hourly_generation": profile_hourly_cool,  # [kWh]
                "supply_temperature": supply_temperature_cool,  # [ºC]
                "target_temperature": target_temperature_cool,  # [ºC]
                "schedule": profile
            }

        }

    except:
        raise ModuleRuntimeException(
            code="1",
            type="building.py",
            msg="Building characterization infeasible. Please check your inputs."
        )


    return streams



