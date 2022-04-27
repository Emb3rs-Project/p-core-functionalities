"""
alisboa/jmcunha


##############################
INFO: Greenhouse Simulation. Simulates the heat needs over the year according to the greenhouse specifications
      and climate weather data of the location

##############################
INPUT: dictionary with:

        Mandatory/Basic User inputs:
            # latitude  []
            # longitude  []
            # width  [m]
            # length  [m]
            # height  [m]
            # greenhouse_orientation
            # saturday_on - 1 (yes)  or 0 (no)
            # sunday_on - 1 (yes)  or 0 (no)
            # shutdown_periods - array with day arrays e.g. [[130,140],[289,299]]
            # daily_periods - array with hour arrays; e.g. [[8,12],[15,19]]
            # lights_on - 1=with lights system ; 0=no lights system
            # hours_lights_needed - lighting hours in greenhouse (counting with daily illuminance) [h]
            # thermal_blanket - 1=with ; 0=no without thermal blanket

            !!!
            IMPORTANT - for Mandatory/Basic User:
                    #  get  greenhouse_efficiency to compute f_c
                        1=tight sealed greenhouse
                        2=medium
                        3=loose

        Optional/Expert User inputs:
            # f_c
            # T_cool_on = in_var.T_cool_on  [ºC]
            # T_heat_on = in_var.T_heat_on  [ºC]
            # supply_temperature_heat [ºC]
            # target_temperature_heat [ºC]
            # leaf_area_index - ratio of area_plants/area_floor, 0 to 1
            # rh_air - controlled interior air RH , 0 to 1
            # u_cover [W/m2.K]
            # indoor_air_speed [m/s]
            # leaf_length - characteristic leaf length [m]
            # tau_cover_long_wave_radiation - 0 to 1
            # emissivity_cover_long_wave_radiation - 0 to 1
            # tau_cover_solar_radiation - 0 to 1
            # power_lights [W/m2]


##############################
OUTPUT: dict with key 'streams' with streams dictionaries, e.g. 'streams' =[stream_1,stream_2, ... :

        Where for example:
        # stream_1 = {
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
import copy
from ....Sink.characterization.Building.Auxiliary.building_climate_api import building_climate_api
from ....Sink.characterization.Building.Auxiliary.wall_area import wall_area
from ....General.Auxiliary_General.schedule_hour import schedule_hour
from ....General.Auxiliary_General.month_last_hour import month_last_hour
from ....Sink.characterization.Building.Auxiliary.h_convection_horizontal import h_convection_horizontal
from ....Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical
from ....Sink.characterization.Building.Auxiliary.ht_radiation_equation import ht_radiation_equation
from ....Sink.characterization.Building.Auxiliary.info_time_step_climate_data import info_time_step_climate_data
from ....Error_Handling.error_greenhouse import error_greenhouse



def greenhouse(in_var):

    ##################################################################################################################
    # INPUT ----------------------------------------------
    # validate inputs
    platform_data = error_greenhouse(in_var['platform'])

    latitude, longitude = platform_data.location
    width = platform_data.width
    length = platform_data.length
    height = platform_data.height
    shutdown_periods = platform_data.shutdown_periods
    daily_periods = platform_data.daily_periods
    greenhouse_orientation = platform_data.greenhouse_orientation
    lights_on = platform_data.lights_on
    T_cool_on = platform_data.T_cool_on
    T_heat_on = platform_data.T_heat_on
    thermal_blanket = platform_data.thermal_blanket
    saturday_on = platform_data.saturday_on
    sunday_on = platform_data.sunday_on
    f_c = platform_data.f_c
    supply_temperature_heat = platform_data.supply_temperature_heat
    target_temperature_heat = platform_data.target_temperature_heat
    leaf_area_index = platform_data.leaf_area_index  # ratio of area_plants/area_floor
    rh_air = platform_data.rh_air  # controlled interior air RH
    u_cover = platform_data.u_cover  # heat transfer coefficient cover [W/m2.K]
    indoor_air_speed = platform_data.indoor_air_speed  # indoor_air_speed [m/s]
    leaf_length = platform_data.leaf_length  # characteristic leaf length [m]
    tau_cover_long_wave_radiation = platform_data.tau_cover_long_wave_radiation  # cover transmissivity long wave radiation
    emissivity_cover_long_wave_radiation = platform_data.emissivity_cover_long_wave_radiation  # emissivity long wave radiation
    tau_cover_solar_radiation = platform_data.tau_cover_solar_radiation  # cover transmissivity solar radiation
    power_lights = platform_data.power_lights  # lighting power per square meter [W/m2]
    hours_lights_needed = platform_data.hours_lights_needed  # lighting hours in greenhouse (counting with daily iluminance) [h]

    ##################################################################################################################
    # DEFINED VARS ----------------------------------------------------------------------------------
    # Greenhouse characteristics
    alpha_plants_and_soil = 0.75
    alpha_greenhouse = tau_cover_solar_radiation * alpha_plants_and_soil
    emissivity_greenhouse = 0.9
    T_ground = 15  # ground temperature [ºC]
    L_ground = 3  # [m]
    k_ground = 1.4  # [W/m.K]
    u_ground = k_ground/L_ground  # [W/m2.K]
    u_thermal_cover = 0.75

    # Fluids Properties
    p_atmospheric = 101  # atmospheric p [kPa]
    rho_air = 1.225  # [kg/m3]
    cp_air = 1005  # [J/kg.K]
    latent_heat_water = 2450 * 1000  # [J/kg]


    ##################################################################################################################
    # COMPUTE ----------------------------------------------------------------------------------
    # Schedule
    profile = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)  # vector: [0,1,1,0,..]; 0-on 1-off
    month_last_hour_vector = month_last_hour()

    # Climate data
    df_climate = building_climate_api(latitude, longitude)

    # Guarantee desired minimum plant illumination
    df_climate['turn_on_lights'] = 0
    save_first_hour = -10  # random value
    save_last_hour = -10


    if lights_on == 1:
        for index, solar_radiation in enumerate(df_climate['Q_sun_roof']):
            if index != 0:
                if solar_radiation > 0 and df_climate.loc[index-1, 'Q_sun_roof'] == 0:
                    save_first_hour = copy.copy(index-1)
                elif solar_radiation == 0 and df_climate.loc[index - 1, 'Q_sun_roof'] > 0:
                    save_last_hour = copy.copy(index)

                if save_first_hour != -10 and save_last_hour != -10 :
                    hours_sun_light = save_last_hour - save_first_hour
                    if hours_sun_light < hours_lights_needed:
                        hours_light_missing = round((hours_lights_needed - hours_sun_light)/2)  # hours of artificial light needed

                        for i in range(hours_light_missing):
                            df_climate.loc[save_first_hour - i, 'turn_on_lights'] = 1
                            df_climate.loc[save_last_hour + i, 'turn_on_lights'] = 1

                    save_first_hour = -10  # reset vars
                    save_last_hour = -10

    # Greenhouse Properties
    area_floor = width * length  # [m2]
    area_plants = area_floor * leaf_area_index
    area_N_wall = wall_area('N', greenhouse_orientation, width, length, height)  # area North facade [m2]
    area_S_wall = wall_area('S', greenhouse_orientation, width, length, height)
    area_E_wall = wall_area('E', greenhouse_orientation, width, length, height)
    area_W_wall = wall_area('W', greenhouse_orientation, width, length, height)
    volume_greenhouse = area_floor * height  # indoor air volume per floor [m3]
    total_cover_area = (area_W_wall + area_N_wall + area_S_wall + area_E_wall + area_floor)


    ##################################################################################################################
    # SIMULATION ----------------------------------------------------------------
    # Initialize vars
    profile_hourly_heat = []
    profile_monthly_heat = []
    profile_monthly_cool = []
    cumulative_heat_monthly = 0
    cumulative_cool_monthly = 0
    T_initial = 15

    if T_initial < T_heat_on:
        T_initial = copy.copy(T_heat_on)
    T_interior = copy.copy(T_initial)  # floor interior air temperature

    # Simulation Info
    time_step = 60*15  # time step [s]
    one_hour = int(3600 / time_step)  # time step number
    max_air_delta_T_per_minute = 1  # 1ºC per min
    max_air_delta_T_allowed = time_step * max_air_delta_T_per_minute / 60

    try:
        for profile_index, profile_operating in enumerate(profile):

            if (profile_index in month_last_hour_vector) or (profile_index == 8759):
                profile_monthly_heat.append(cumulative_heat_monthly)  # space heating demand [kWh]
                profile_monthly_cool.append(cumulative_cool_monthly)  # space cooling demand [kWh]
                cumulative_heat_monthly = 0  # reset monthly heating needs
                cumulative_cool_monthly = 0  # reset monthly cooling needs

            if profile_index == 8759:
                break

            cumulative_heat_hourly = 0  # reset hourly heating needs

            for i in range(one_hour):
                # CLIMATE DATA --------------------------------------------------------------------------------------
                T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed = info_time_step_climate_data(
                    df_climate, profile_index, one_hour, i)

                if thermal_blanket == 1:
                    if Q_sun_roof <= 80:  # simplification to determine when blanket is covering greenhouse
                        Q_sun_roof = 0

                # Correct wind speed
                z_0 = 0.01 # surface roughness
                wind_speed = wind_speed * (math.log((height/2) / z_0)) / (math.log(10 / z_0))
                u_exterior = (5.8 + 3.94 * wind_speed)  # outside heat convection coef. [W/m2.K]

                # GREENHOUSE Heat balance --------------------------------------------------------------------------------
                # Solar radiation
                Q_sun_greenhouse = (Q_sun_roof * area_floor) * alpha_greenhouse

                # Infiltrations
                f_t = 0.16
                c_w = 0.22
                area_infiltration = total_cover_area * f_c
                air_change_per_second = area_infiltration * math.sqrt(
                    c_w ** 2 * wind_speed + f_t ** 2 * (abs(T_interior - T_exterior)))  # [m3/s]

                # Evapotranspiration
                vapour_p_plants = (math.exp(20.386 - 5132 / (T_interior + 273.1))) * 0.13  # [kPa]
                vapour_p_air = (math.exp(20.386 - 5132 / (T_interior + 273.1))) * (rh_air/100) * 0.13  # [kPa]
                w_plant = 0.6219 * vapour_p_plants / (p_atmospheric - vapour_p_plants)  # [kg_water/kg_air]
                w_air = 0.6219 * vapour_p_air / (p_atmospheric - vapour_p_air)
                R_aerodynamic = 220 * (leaf_length ** 0.2) / (indoor_air_speed ** 0.8)
                R_stomatal = 200 * (1 + 1 / (math.exp(0.05 * (Q_sun_roof * alpha_greenhouse - 50))))
                m_evap_water = area_plants * rho_air * (w_plant - w_air) / (R_aerodynamic + R_stomatal)  # [kg/s]

                if m_evap_water < 0:
                    m_evap_water = 0

                Q_plants = m_evap_water * latent_heat_water  # [W]

                # Conduction Ground Losses
                Q_lost_ground = u_ground * area_floor * (T_ground - T_interior)

                # Convection Cover Losses
                T_cover = 2 / 3 * T_exterior + T_interior * 1 / 3  # average T_cover [ºC]
                h_vertical = h_convection_vertical(T_cover, T_interior)
                h_horizontal = h_convection_horizontal(T_cover, T_interior)

                coef_horizontal = 1
                coef_vertical = 1
                if h_horizontal == 0:
                    h_horizontal = 1
                    coef_horizontal = 0
                if h_vertical == 0:
                    h_vertical = 1
                    coef_vertical = 0

                if Q_sun_greenhouse == 0 and thermal_blanket == 1:
                    val_thermal_blanket = 1
                else:
                    val_thermal_blanket = 0

                u_horizontal = (1 / u_cover + 1 / u_thermal_cover * val_thermal_blanket + 1 / u_exterior + 1 / h_horizontal * coef_horizontal) ** (-1)
                u_vertical = (1 / u_cover + 1 / u_thermal_cover * val_thermal_blanket + 1 / u_exterior + 1 / h_vertical * coef_vertical) ** (-1)
                Q_top = area_floor * u_horizontal * (T_exterior - T_interior)
                Q_vertical_wall_small = area_E_wall * u_vertical * (T_exterior - T_interior)
                Q_vertical_wall_big = area_N_wall * u_vertical * (T_exterior - T_interior)
                Q_lost_exterior = Q_top + 2 * (Q_vertical_wall_small + Q_vertical_wall_big)

                # Radiation Losses
                if Q_sun_greenhouse == 0:
                    Q_rad_lost = 0
                else:
                    view_factor = 1
                    area_sky = total_cover_area
                    Q_rad_sky = ht_radiation_equation(emissivity_greenhouse, area_sky, T_interior, T_sky,
                                                      view_factor) * tau_cover_long_wave_radiation
                    Q_rad_ground = ht_radiation_equation(emissivity_cover_long_wave_radiation, area_sky, T_interior,
                                                         T_cover, view_factor)
                    Q_rad_lost = (Q_rad_sky + Q_rad_ground)  # [W]

                # Infiltration
                Q_infiltrations = rho_air * cp_air * air_change_per_second * (T_exterior - T_interior)

                # Lights
                if df_climate.loc[profile_index, 'turn_on_lights'] == 1:
                    Q_lights = power_lights * area_floor
                else:
                    Q_lights = 0

                # Greenhouse Air Heat Balance
                Q_greenhouse = Q_lights + \
                               Q_infiltrations + \
                               Q_lost_ground + \
                               Q_lost_exterior + \
                               Q_sun_greenhouse - \
                               Q_plants + \
                               Q_rad_lost

                # SPACE HEATING/COOLING ACTUATION
                # on work time
                if profile_operating == 1:
                    T_interior_guess = T_interior + Q_greenhouse * time_step / (rho_air * cp_air * volume_greenhouse)
                    # activating space heating
                    if T_interior < T_heat_on and T_interior_guess < T_heat_on:
                        if Q_greenhouse < 0:
                            if T_heat_on - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = abs(Q_greenhouse) + (rho_air * cp_air * volume_greenhouse) * (
                                        T_heat_on - T_interior) / time_step
                            else:
                                Q_heat_required = abs(Q_greenhouse) + (
                                        rho_air * cp_air * volume_greenhouse) * max_air_delta_T_allowed / time_step
                        else:
                            if T_interior_guess - T_interior < max_air_delta_T_allowed:
                                Q_heat_required = (rho_air * cp_air * volume_greenhouse) * (
                                        max_air_delta_T_allowed - (T_interior_guess - T_interior)) / time_step
                            else:
                                Q_heat_required = 0

                    elif T_interior >= T_heat_on and T_interior_guess < T_heat_on:
                        Q_heat_required = (rho_air * cp_air * volume_greenhouse) * (
                                T_heat_on - T_interior_guess) / time_step

                    else:
                        Q_heat_required = 0
                else:
                    Q_heat_required = 0

                # COMPUTE INTERIOR TEMPERATURE
                T_interior = T_interior + (Q_greenhouse + Q_heat_required) * time_step / (
                            rho_air * cp_air * volume_greenhouse)  # [ºC]

                if T_interior >= T_cool_on and T_cool_on >= T_exterior:
                    T_interior = T_cool_on
                elif T_interior >= T_cool_on and T_exterior >= T_cool_on:
                    T_interior = T_exterior

                # Data Profiles
                if Q_heat_required > 0:
                    cumulative_heat_monthly += Q_heat_required * time_step / 3600000  # [kW]
                    cumulative_heat_hourly += Q_heat_required * time_step / 3600000

            # Hourly Profiles
            profile_hourly_heat.append(cumulative_heat_hourly)  # space heating demand [kWh]

        # OUTPUT -------------
        output = {
            'hot_stream': {
                'id': 1,
                'object_id': None,
                'object_type': 'stream_building',
                'fluid': 'water',
                'stream_type': 'inflow',
                'capacity': max(profile_hourly_heat),
                "monthly_generation": profile_monthly_heat,  # [kWh]
                "hourly_generation": profile_hourly_heat,  # [kWh]
                "supply_temperature": supply_temperature_heat,  # [ºC]
                "target_temperature": target_temperature_heat,  # [ºC]
                "schedule": profile
            }
        }


    except:
        raise Exception("Greenhouse Simulation not feasible. Please, check your inputs")


    return output




