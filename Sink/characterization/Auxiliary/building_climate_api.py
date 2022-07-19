import math
import numpy as np
import pvlib
import datetime
import pandas as pd


def building_climate_api(latitude,longitude):
    """Get climate data for a specific location, for the building/greenhouse routine

    Returns  incident solar radiation in each building' facade [W/m2], ambient and sky temperatures [ºC], and wind
    speed at 10m [m/s].

    Parameters
    ----------
    latitude : float
        Location latitude [º]

    longitude : float
        Location longitude [º]

    Returns
    -------
    df_output : df
        dataframe with climate data, with the following keys:

            T_exterior : float
                Ambient temperature [ºC]

            T_sky : float
                Sky temperature [ºC]

            Q_beam_solar_collector : float
                Direct/Beam solar radiation [W]

            Q_dif_solar_collector : float
                Diffuse solar radiation [W]

            Q_sun_N_facade : float
                Incident solar radiation on the North Facade [W]

            Q_sun_S_facade : float

            Q_sun_E_facade : float

            Q_sun_W_facade : float

            Q_sun_roof : float

            Wind_speed : float
                Wind speed [m/s]

    """

    # Building data
    N_azimuth = 180
    S_azimuth = N_azimuth - 180
    E_azimuth = N_azimuth - 270
    W_azimuth = N_azimuth - 90
    wall_inclination = 90
    solar_collector_inclination = latitude - 15

    # Get Climate Data from API
    raw_df = pvlib.iotools.get_pvgis_tmy(latitude, longitude, outputformat='csv', usehorizon=True, userhorizon=None, startyear=None, endyear=None, url='https://re.jrc.ec.europa.eu/api/', timeout=30, map_variables=False)

    climate_df = raw_df[0]

    data = np.zeros((8760,832))

    elevation = raw_df[2]["elevation"]
    data[:, 0] = climate_df['T2m'] - 0.00356 * elevation  #Ambient temperature [ºC]
    data[:, 1] = climate_df['RH'] # Relatitudeive Humidity [%]
    data[:, 3] = climate_df['G(h)'] # Global horizontal irradiance [Wh/m2]
    data[:, 4] = climate_df['Gb(n)'] # Direct normal irradiance [Wh/m2]
    data[:, 5] = climate_df['Gd(h)'] # Global diffuse horizontal irradiance [Wh/m2]
    data[:, 6] = climate_df['IR(h)'] # Infrared horizontal irradiance [Wh/m2]
    data[:, 7] = climate_df['WS10m'] # Infrared horizontal irradiance [Wh/m2]

    # Create Output DF
    df_col_names = ['T_exterior','T_sky','Q_sun_N_facade','Q_sun_S_facade','Q_sun_E_facade', 'Q_sun_W_facade','Q_sun_roof','Q_solar_collector']
    df_output = pd.DataFrame(columns=df_col_names)

    new_rows = []

    for i in range(8760):

        T_sky = (data[i,6]/(0.0000000567))**0.25-273
        day = i/24
        GMT = i-np.floor((i)/24)*24+1
        gamma = 2*np.radians(180)/365*day
        ET = 229.18*(0.000075 + 0.001868*np.cos(gamma) -0.032077 *np.sin(gamma)-0.01465*np.cos(2*gamma)-0.040849*np.sin(2*gamma))
        TSV = GMT+ET/60-12
        Ah = TSV*15
        year_now = datetime.datetime.now().year
        u = day-79.301-0.02422*(year_now-1969)+int(((year_now-1969)/4))
        declin = 0.3723+23.2567*math.sin(math.radians(0.985647*u))+0.1149*math.sin(math.radians(2*u*0.985647))-0.1712*math.sin(math.radians(3*u*0.985647))-0.758*math.cos(math.radians(u*0.985647))+0.3656*math.cos(math.radians(2*u*0.985647))+0.0201*math.cos(math.radians(3*u*0.985647))
        v01 = math.asin(math.sin(math.radians(declin))*math.sin(math.radians(latitude))+math.cos(math.radians(declin))*math.cos(math.radians(latitude))*math.cos(math.radians(Ah)))
        v02 = math.degrees(math.asin(math.cos(math.radians(declin))*math.sin(math.radians(Ah))/math.cos(v01)))

        # Sun Azimuth
        if v02 < 0:
            sun_azimuth = -1 * math.degrees(math.acos((math.sin(v01) * math.sin(math.radians(latitude)) - math.sin(math.radians(declin))) / (math.cos(v01) * math.cos(math.radians(latitude)))))
        else:
            sun_azimuth = math.degrees(math.acos((math.sin(v01) * math.sin(math.radians(latitude)) - math.sin(math.radians(declin))) / ( math.cos(v01) * math.cos(math.radians(latitude)))))

        # Sun Altitude
        if math.asin(math.sin(math.radians(declin)) * math.sin(math.radians(latitude)) + math.cos(math.radians(declin)) * math.cos(math.radians(latitude)) * math.cos(math.radians(Ah))) < 0:
            sun_altitude = 0
        else:
            sun_altitude = math.asin(math.sin(math.radians(declin)) * math.sin(math.radians(latitude)) + math.cos(math.radians(declin)) * math.cos(math.radians(latitude)) * math.cos(math.radians(Ah)))

        # Solar radiation on surfaces
        if sun_altitude == 0:
            Q_sun_N_facade = 0
            Q_sun_S_facade = 0
            Q_sun_E_facade = 0
            Q_sun_W_facade = 0
            Q_sun_roof = data[i, 3]
            Q_solar_collector = 0

        else:
            N_wall_incidence_angle = math.acos(math.sin(sun_altitude) * math.cos(math.radians(wall_inclination)) + math.cos(sun_altitude) * math.sin(math.radians(wall_inclination)) * math.cos(math.radians(abs(N_azimuth - sun_azimuth))))
            S_wall_incidence_angle = math.acos(math.sin(sun_altitude) * math.cos(math.radians(wall_inclination)) + math.cos(sun_altitude) * math.sin(math.radians(wall_inclination)) * math.cos(math.radians(abs(S_azimuth - sun_azimuth))))
            E_wall_incidence_angle = math.acos(math.sin(sun_altitude) * math.cos(math.radians(wall_inclination)) + math.cos(sun_altitude) * math.sin(math.radians(wall_inclination)) * math.cos(math.radians(abs(E_azimuth - sun_azimuth))))
            W_wall_incidence_angle = math.acos(math.sin(sun_altitude) * math.cos(math.radians(wall_inclination)) + math.cos(sun_altitude) * math.sin(math.radians(wall_inclination)) * math.cos(math.radians(abs(W_azimuth - sun_azimuth))))

            roof_incidence_angle = math.acos(math.sin(sun_altitude))
            solar_collector_incidence_angle = math.acos(math.sin(sun_altitude) * math.cos(math.radians(solar_collector_inclination)) + math.cos(sun_altitude) * math.sin(math.radians(solar_collector_inclination)) * math.cos(math.radians(sun_azimuth)))

            if math.degrees(N_wall_incidence_angle) > 90:
                N_wall_incidence_angle = math.radians(90)
            if math.degrees(S_wall_incidence_angle) > 90:
                S_wall_incidence_angle = math.radians(90)
            if math.degrees(E_wall_incidence_angle) > 90:
                E_wall_incidence_angle = math.radians(90)
            if math.degrees(W_wall_incidence_angle) > 90:
                W_wall_incidence_angle = math.radians(90)
            if math.degrees(roof_incidence_angle) > 90:
                roof_incidence_angle = math.radians(90)
            if math.degrees(solar_collector_incidence_angle) > 90:
                solar_collector_incidence_angle = math.radians(90)

            Q_sun_N_facade = data[i, 4] * math.cos(N_wall_incidence_angle) + (180 - wall_inclination) / (180) * data[i, 5]  # direct and dif. solar radiation correction on the facade
            Q_sun_S_facade = data[i, 4] * math.cos(S_wall_incidence_angle) + (180 - wall_inclination) / (180) * data[i, 5]
            Q_sun_E_facade = data[i, 4] * math.cos(E_wall_incidence_angle) + (180 - wall_inclination) / (180) * data[i, 5]
            Q_sun_W_facade = data[i, 4] * math.cos(W_wall_incidence_angle) + (180 - wall_inclination) / (180) * data[i, 5]
            Q_solar_collector = data[i, 4] * math.cos(solar_collector_incidence_angle)
            Q_sun_roof = data[i, 3]


        # OUTPUT
        new_row = {'T_exterior': data[i, 0],
                   'T_sky': T_sky,
                   'Q_sun_N_facade': Q_sun_N_facade,
                   'Q_sun_S_facade': Q_sun_S_facade,
                   'Q_sun_E_facade': Q_sun_E_facade,
                   'Q_sun_W_facade': Q_sun_W_facade,
                   'Q_sun_roof': Q_sun_roof,
                   'Q_solar_collector': Q_solar_collector,
                   'Wind_speed': data[i, 7],
                   }


        new_rows.append(new_row)

    df_output = pd.DataFrame(new_rows)

   # df_output = df_output.concat(df_output.tail(n=24), ignore_index=True)
    df_output = pd.concat([df_output,df_output.tail(n=24)], ignore_index=True)


    return df_output


