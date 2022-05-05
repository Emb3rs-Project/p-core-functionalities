"""
alisboa/jmcunha


##############################
INFO: Interpolate climate data to estimate each value for the current time step.


##############################
INPUT:
        # df_climate - df with all climate parameters needed from building_climate_api
        # profile_index
        # one_hour
        # time_instant - present time step


##############################
OUTPUT:
        # T_exterior  [ºC]
        # T_sky  [ºC]
        # Q_sun_N_facade  [W]
        # Q_sun_S_facade  [W]
        # Q_sun_E_facade  [W]
        # Q_sun_W_facade  [W]
        # Q_sun_roof  [W]
        # wind_speed  [m/s]


"""

from ....General.Auxiliary_General.interpolation import interpolation


def info_time_step_climate_data(df_climate, profile_index, one_hour, time_instant):

    T_exterior = interpolation(df_climate.loc[profile_index + 1, 'T_exterior'],
                               df_climate.loc[profile_index, 'T_exterior'], one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'T_exterior'])  # Ambient temperature [ºC]

    T_sky = interpolation(df_climate.loc[profile_index + 1, 'T_sky'], df_climate.loc[profile_index, 'T_sky'], one_hour,
                          0, time_instant, df_climate.loc[profile_index, 'T_sky'])  # Sky temperature [ºC]

    Q_sun_N_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_N_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_N_facade'], one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_N_facade'])  # Incident radiation [W/m2]

    Q_sun_S_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_S_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_S_facade'], one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_S_facade'])

    Q_sun_E_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_E_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_E_facade'], one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_E_facade'])

    Q_sun_W_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_W_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_W_facade'], one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_W_facade'])

    Q_sun_roof = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_roof'],
                               df_climate.loc[profile_index, 'Q_sun_roof'], one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'Q_sun_roof'])

    wind_speed = interpolation(df_climate.loc[profile_index + 1, 'Wind_speed'],
                               df_climate.loc[profile_index, 'Wind_speed'], one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'Wind_speed'])  # [m/s]

    return T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed
