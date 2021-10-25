""""

Info: Compute Greenhouse Heating demand profile, according to the user's specifications.


"""

import json
import math
from Sink.characterization.Building.Auxiliary.building_climate_api import building_climate_api
from Sink.characterization.Building.Auxiliary.wall_area import wall_area
from General.Auxiliary_General.schedule_hour import schedule_hour
import copy
from General.Auxiliary_General.month_last_hour import month_last_hour
from Sink.characterization.Building.Auxiliary.h_convection_horizontal import h_convection_horizontal
from Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical
from Sink.characterization.Building.Auxiliary.ht_radiation_equation import ht_radiation_equation
from Sink.characterization.Building.Auxiliary.info_time_step_climate_data import info_time_step_climate_data


def greenhouse(in_var):

    building_type = in_var.building_type

    # INPUT ----------------------------------------------
    latitude = in_var.latitude
    longitude = in_var.longitude
    width_floor = in_var.width  # [m]
    length_floor = in_var.length  # [m]
    height_floor = in_var.height_floor  # [m]
    shutdown_periods = in_var.shutdown_periods
    daily_periods = in_var.daily_periods
    building_orientation = in_var.building_orientation
    saturday_on = in_var.saturday_on
    sunday_on = in_var.sunday_on

    #####################################################
    #####################################################
    #####################################################
    # User input or defined

    f_c = in_var.f_c  # Building efficiency - 1=A to 3=F
    T_cool_on = in_var.T_cool_on  # cooling start temperature working hours [ºC]
    T_heat_on = in_var.T_heat_on  # heating start temperature working hours [ºC]
    supply_temperature_heat = in_var.supply_temperature_heat
    target_temperature_heat = in_var.target_temperature_heat
    leaf_area_index = in_var.leaf_area_index  # ratio of area_plants/area_floor
    rh_air = in_var.rh_air  # controlled interior air RH
    u_cover = in_var.u_cover  # heat transfer coefficient cover [W/m2.K]
    indoor_air_speed = in_var.indoor_air_speed  # indoor_air_speed [m/s]
    leaf_length = in_var.leaf_length  # characteristic leaf length [m]
    tau_cover_long_wave_radiation = in_var.tau_cover_long_wave_radiation  # cover transmissivity long wave radiation
    emissivity_cover_long_wave_radiation = in_var.emissivity_cover_long_wave_radiation  # emissivity long wave radiation
    tau_cover_solar_radiation = in_var.tau_cover_solar_radiation  # cover transmissivity solar radiation
    lights_on = in_var.lights_on  # 1- with lights system ; 0 - no lights system
    hours_lights_needed = in_var.hours_lights_needed  # lighting hours in greenhouse (counting with daily iluminance) [h]
    power_lights = in_var.power_lights  # lighting power per square meter [W/m2]


    # DEFINED VARS ----------------------------------------------------------------------------------
    # Ground characteristics
    T_ground = 15  # ground temperature [ºC]
    L_ground = 3  # [m] - https://www.researchgate.net/publication/245189597_Spatial_variability_of_soil_temperature_under_greenhouse_conditions
    k_ground = 1.4  # [W/m.K]
    u_ground = k_ground/L_ground # ground thermal conductivity/ height to constant floor T -

    # Greenhouse characteristics
    alpha_greenhouse = 0.75  # - ref:https://doi.org/10.1016/j.inpa.2017.12.003
    emissivity_greenhouse = 0.9

    # Fluids/Material Properties
    pressure_atmospheric = 101  # atmospheric pressure [kPa]
    rho_air = 1.225  # [kg/m3]
    cp_air = 1005  # [J/kg.K]
    latent_heat_water = 2450 * 1000  # [J/kg]


    # COMPUTE ----------------------------------------------
    # Schedule
    profile = schedule_hour(saturday_on, sunday_on, shutdown_periods, daily_periods)  # vector: [0,1,1,0,..]; 0-on 1-off
    month_last_hour_vector = month_last_hour()

    # Climate data
    df_climate = building_climate_api(latitude, longitude)

    # Guarantee desired minimum plant illumination
    df_climate['turn_on_lights'] = 0
    save_first_hour = -10 # random value below 0
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
    area_floor = width_floor*length_floor  # [m2]
    area_plants = area_floor * leaf_area_index
    area_N_wall = wall_area('N', building_orientation, width_floor, length_floor, height_floor)  # area North facade [m2]
    area_S_wall = wall_area('S', building_orientation, width_floor, length_floor, height_floor)
    area_E_wall = wall_area('E', building_orientation, width_floor, length_floor, height_floor)
    area_W_wall = wall_area('W', building_orientation, width_floor, length_floor, height_floor)
    volume_greenhouse = area_floor * height_floor  # indoor air volume per floor [m3]
    total_cover_area = area_W_wall + area_N_wall + area_S_wall + area_E_wall + area_floor

    # SIMULATION ----------------------------------------------------------------
    # Initialize vars
    profile_hourly_heat = []
    profile_hourly_cool = []
    profile_monthly_heat = []
    profile_monthly_cool = []
    cumulative_heat_monthly = 0
    cumulative_cool_monthly = 0

    T_initial = df_climate.loc[0, 'T_exterior']

    if T_initial < T_heat_on:
        T_initial = T_heat_on

    T_interior = copy.copy(T_initial)  # floor interior air temperature

    # Simulation Info
    time_step = 1000  # time step [s]
    one_hour = int(3600 / time_step)  # time step number
    max_air_delta_T_per_minute = 1  # 1ºC per min
    max_air_delta_T_allowed = time_step * max_air_delta_T_per_minute / 60

    for profile_index, profile_operating in enumerate(profile):

        if (profile_index in month_last_hour_vector) or (profile_index == 8759):
            profile_monthly_heat.append(cumulative_heat_monthly)  # space heating demand [kWh]
            profile_monthly_cool.append(cumulative_cool_monthly)  # space cooling demand [kWh]
            cumulative_heat_monthly = 0  # reset monthly heating needs
            cumulative_cool_monthly = 0  # reset monthly cooling needs

        if profile_index == 8759:
            break  # safety

        cumulative_heat_hourly = 0  # reset hourly heating needs
        cumulative_cool_hourly = 0  # reset hourly cooling needs

        for i in range(one_hour):
            # CLIMATE DATA --------------------------------------------------------------------------------------
            T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed = info_time_step_climate_data(df_climate,profile_index,one_hour,i)

            # Correct wind speed
            z_0 = 0.01 # surface roughness
            wind_speed = wind_speed * (math.log((height_floor/2) / z_0)) / (math.log(10 / z_0))
            u_exterior = (5.8 + 3.94 * wind_speed)  # outside heat convection coef. [W/m2.K] - ref: doi:10.1016/j.applthermaleng.2007.12.005


            # GREENHOUSE  --------------------------------------------------------------------------------------
            # Solar radiation greenhouse
            Q_sun_greenhouse = (Q_sun_N_facade * area_N_wall + Q_sun_S_facade * area_S_wall + Q_sun_E_facade * area_E_wall + Q_sun_W_facade * area_W_wall + Q_sun_roof * area_floor) * tau_cover_solar_radiation  # [W]

            # Infiltrations/ACH - https://doi.org/10.1016/j.compag.2018.04.025
            f_t = 0.16
            c_w = 0.22
            area_infiltration = total_cover_area * f_c
            ACH = area_infiltration * math.sqrt(c_w ** 2 * wind_speed + f_t**2*(abs(T_interior-T_exterior)))  # [m3/s]

            # Evapotranspiration - ref:https://doi.org/10.1016/j.inpa.2017.12.003
            vapour_pressure_plants = (math.exp(20.386 - 5132 / (T_interior + 273.1))) * 0.13  # [kPa]
            vapour_pressure_air = (math.exp(20.386 - 5132 / (T_interior + 273.1))) * rh_air * 0.13  # [kPa]
            w_plant = 0.6219 * vapour_pressure_plants / (pressure_atmospheric - vapour_pressure_plants)  # [kg_water/kg_air]
            w_air = 0.6219 * vapour_pressure_air / (pressure_atmospheric - vapour_pressure_air)
            aerodynamic_resistance = 220 * (leaf_length ** 0.2 )/ (indoor_air_speed ** 0.8)
            stomatal_resistance = 200 * (1 + 1 / (math.exp(0.05 * (Q_sun_roof*tau_cover_solar_radiation - 50))))

            m_evap_water = area_plants * rho_air * (w_plant - w_air) / (aerodynamic_resistance + stomatal_resistance)  # [kg/s]

            if m_evap_water < 0:
                m_evap_water = 0

            Q_plants = m_evap_water * latent_heat_water  # [W]

            # Exterior Losses - ref:https://doi.org/10.1016/j.inpa.2017.12.003
            T_cover = 2 / 3 * T_exterior + T_interior * 1 / 3  # average T_cover [ºC]
            u_total = (1/u_cover + 1/u_exterior)**(-1)  # [W/m2.K]

            Q_lost_exterior = u_total * total_cover_area * (T_exterior - T_interior)

            # Ground Losses
            Q_lost_ground = u_ground * area_floor * (T_ground - T_interior)

            # Sky Losses
            view_factor = 1
            Q_rad_sky = ht_radiation_equation(emissivity_greenhouse, area_floor, T_interior, T_sky, view_factor) * tau_cover_long_wave_radiation
            Q_rad_ground = ht_radiation_equation(emissivity_cover_long_wave_radiation, total_cover_area, T_interior, T_cover, view_factor)
            Q_rad_lost = Q_rad_sky + Q_rad_ground  # [W]

            # Cover Convection
            h_vertical = h_convection_vertical(T_cover, T_interior)
            Q_vertical_wall_big = (T_cover - T_interior) * h_vertical * area_N_wall
            Q_vertical_wall_small = (T_cover - T_interior) * h_vertical * area_E_wall

            h_horizontal = h_convection_horizontal(T_cover, T_interior)
            Q_top = (T_cover - T_interior) * h_horizontal * area_floor
            Q_conv_total = Q_top + 2 * (Q_vertical_wall_small + Q_vertical_wall_big)

            # Infiltration
            Q_infiltrations = rho_air * cp_air * ACH * (T_exterior - T_interior)

            # Lights
            if df_climate.loc[profile_index, 'turn_on_lights'] == 1:
                Q_lights = power_lights*area_floor
            else:
                Q_lights = 0

            # Greenhouse Air Heat Balance
            Q_greenhouse = Q_lights + \
                           Q_infiltrations + \
                           Q_conv_total +  \
                           Q_lost_ground +  \
                           Q_lost_exterior + \
                           Q_sun_greenhouse*alpha_greenhouse - \
                           Q_plants +  \
                           Q_rad_lost


            # SPACE HEATING/COOLING ACTUATION --------------------------------------------------------
            # on work time
            if profile_operating == 1:
                T_interior_guess = T_interior + (Q_greenhouse) * time_step / (rho_air * cp_air * volume_greenhouse)

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

                # activating space heating
                elif T_interior >= T_heat_on and T_interior_guess < T_heat_on:
                    Q_heat_required = (rho_air * cp_air * volume_greenhouse) * (T_heat_on - T_interior_guess) / time_step

                else:
                    Q_heat_required = 0
            else:
                Q_heat_required = 0


            # COMPUTE INTERIOR TEMPERATURE  --------------------------------------------------------
            # Explicit T_interior computation
            T_interior = T_interior + (Q_greenhouse + Q_heat_required) * time_step / (rho_air * cp_air * volume_greenhouse)  # [ºC]

            if T_interior >= T_cool_on and T_cool_on >= T_exterior:
                T_interior = T_cool_on
            elif T_interior >= T_cool_on and T_exterior >= T_cool_on:
                T_interior = T_exterior


            # Data Profiles
            if Q_heat_required > 0:
                cumulative_heat_monthly += Q_heat_required * time_step / 3600000  # [kW]
                cumulative_heat_hourly += Q_heat_required * time_step / 3600000
            else:
                cumulative_cool_monthly += 0
                cumulative_cool_hourly += 0

        # Hourly Profiles
        profile_hourly_heat.append(cumulative_heat_hourly)  # space heating demand [kWh]
        profile_hourly_cool.append(cumulative_cool_hourly)  # space cooling demand [kWh]


    # OUTPUT -------------
    output = {
        'id': 7777,
        'object_type': 'stream',
        'fluid': 'water',
        "monthly_generation": profile_monthly_heat,  # [kWh]
        "hourly_generation": profile_hourly_heat,  # [kWh]
        "supply_temperature": supply_temperature_heat,  # [ºC]
        "target_temperature": target_temperature_heat,  # [ºC]
    }

    output = json.dumps(output, indent=2)

    return output




