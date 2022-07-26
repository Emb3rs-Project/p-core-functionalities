from ....General.Auxiliary_General.interpolation import interpolation


def info_time_step_climate_data(df_climate, profile_index, time_step_number_in_one_hour, time_instant):
    """Interpolate climate data to estimate each value for the current time step

    Parameters
    ----------
    df_climate : df
        df with all climate parameters needed from building_climate_api

    profile_index: int
        Index

    time_step_number_in_time_step_number_in_one_hour: int

    time_instant : float
        Present time step

    Returns
    -------
    T_exterior : float
        Ambient temperature [ºC]

    T_sky : float
        Sky temperature [ºC]

    Q_sun_N_facade : float
        Solar radiation on the specified surface [W]

    Q_sun_S_facade : float
        Solar radiation on the specified surface [W]

    Q_sun_E_facade : float
        Solar radiation on the specified surface [W]

    Q_sun_W_facade : float
        Solar radiation on the specified surface [W]

    Q_sun_roof : float
        Solar radiation on the specified surface [W]

    wind_speed : float
        [m/s]

    """

    T_exterior = interpolation(df_climate.loc[profile_index + 1, 'T_exterior'],
                               df_climate.loc[profile_index, 'T_exterior'], time_step_number_in_one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'T_exterior'])  # Ambient temperature [ºC]

    T_sky = interpolation(df_climate.loc[profile_index + 1, 'T_sky'], df_climate.loc[profile_index, 'T_sky'], time_step_number_in_one_hour,
                          0, time_instant, df_climate.loc[profile_index, 'T_sky'])  # Sky temperature [ºC]

    Q_sun_N_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_N_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_N_facade'], time_step_number_in_one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_N_facade'])  # Incident radiation [W/m2]

    Q_sun_S_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_S_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_S_facade'], time_step_number_in_one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_S_facade'])

    Q_sun_E_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_E_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_E_facade'], time_step_number_in_one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_E_facade'])

    Q_sun_W_facade = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_W_facade'],
                                   df_climate.loc[profile_index, 'Q_sun_W_facade'], time_step_number_in_one_hour, 0, time_instant,
                                   df_climate.loc[profile_index, 'Q_sun_W_facade'])

    Q_sun_roof = interpolation(df_climate.loc[profile_index + 1, 'Q_sun_roof'],
                               df_climate.loc[profile_index, 'Q_sun_roof'], time_step_number_in_one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'Q_sun_roof'])

    wind_speed = interpolation(df_climate.loc[profile_index + 1, 'Wind_speed'],
                               df_climate.loc[profile_index, 'Wind_speed'], time_step_number_in_one_hour, 0, time_instant,
                               df_climate.loc[profile_index, 'Wind_speed'])  # [m/s]

    return T_exterior, T_sky, Q_sun_N_facade, Q_sun_S_facade, Q_sun_E_facade, Q_sun_W_facade, Q_sun_roof, wind_speed
