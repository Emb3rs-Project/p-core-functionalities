""""
alisboa/jmcunha


##############################
INFO: Get climatic conditions according to the location in a hourly profile.


##############################
INPUT:
        # latitude  [º]
        # longitude  [º]


##############################
RETURN: df (year hourly profile) with:

        # T_exterior
        # T_sky
        # Q_beam_solar_collector
        # Q_dif_solar_collector


"""

import numpy as np
import math
import pvlib
import datetime
import pandas as pd


def solar_collector_climate_api(latitude,longitude):

    # Initialize Arrays ------
    solar_collector_inclination = latitude - 15

    # Create Output DF
    df_col_names = ['T_exterior','T_sky','Q_beam_solar_collector','Q_dif_solar_collector']
    df_output = pd.DataFrame(columns=df_col_names)

    # Get Climate Data from API
    raw_df = pvlib.iotools.get_pvgis_tmy(latitude, longitude, outputformat='csv', usehorizon=True, userhorizon=None, startyear=None, endyear=None, url='https://re.jrc.ec.europa.eu/api/', timeout=30)
    climate_df = raw_df[0]
    data = np.zeros((8760,7))
    data[:, 0] = climate_df['T2m']  # Ambient temperature [ºC]
    data[:, 1] = climate_df['RH']  # Relatitudeive Humidity [%]
    data[:, 3] = climate_df['G(h)']  # Global horizontal irradiance [Wh/m2]
    data[:, 4] = climate_df['Gb(n)']  # Direct normal irradiance [Wh/m2]
    data[:, 5] = climate_df['Gd(h)']  # Global diffuse horizontal irradiance [Wh/m2]
    data[:, 6] = climate_df['IR(h)']  # Infrared horizontal irradiance [Wh/m2]

    # COMPUTE ------
    for i in range (8760):
        T_sky = (data[i,6]/(0.0000000567))**0.25-273
        day = i/24
        GMT = i-np.floor((i)/24)*24 + 1
        gamma = 2*np.radians(180)/365*day
        ET = 229.18*(0.000075  +  0.001868*np.cos(gamma) -0.032077 *np.sin(gamma)-0.01465*np.cos(2*gamma)-0.040849*np.sin(2*gamma))
        TSV = GMT + ET/60-12
        Ah = TSV*15
        year_now = datetime.datetime.now().year
        u = day-79.301-0.02422*(year_now-1969) + int(((year_now-1969)/4))
        declin = 0.3723 + 23.2567*math.sin(math.radians(0.985647*u)) + 0.1149*math.sin(math.radians(2*u*0.985647))-0.1712*math.sin(math.radians(3*u*0.985647))-0.758*math.cos(math.radians(u*0.985647)) + 0.3656*math.cos(math.radians(2*u*0.985647)) + 0.0201*math.cos(math.radians(3*u*0.985647))
        v01 = math.asin(math.sin(math.radians(declin))*math.sin(math.radians(latitude)) + math.cos(math.radians(declin))*math.cos(math.radians(latitude))*math.cos(math.radians(Ah)))
        v02 = math.degrees(math.asin(math.cos(math.radians(declin))*math.sin(math.radians(Ah))/math.cos(v01)))

        # Sun Azimuth
        if v02<0:
           sun_azimuth = -1*math.degrees(math.acos((math.sin(v01)*math.sin(math.radians(latitude))-math.sin(math.radians(declin)))/(math.cos(v01)*math.cos(math.radians(latitude)))))
        else:
           sun_azimuth = math.degrees(math.acos((math.sin(v01)*math.sin(math.radians(latitude))-math.sin(math.radians(declin)))/(math.cos(v01)*math.cos(math.radians(latitude)))))

        # Sun Altitude
        if math.asin(math.sin(math.radians(declin))*math.sin(math.radians(latitude)) + math.cos(math.radians(declin))*math.cos(math.radians(latitude))*math.cos(math.radians(Ah)))<0:
            sun_altitude = 0
        else:
            sun_altitude = math.asin(math.sin(math.radians(declin))*math.sin(math.radians(latitude)) + math.cos(math.radians(declin))*math.cos(math.radians(latitude))*math.cos(math.radians(Ah)))

        # Direct solar radiation on solar collector
        if sun_altitude == 0:
            Q_beam_solar_collector = 0
            Q_dif_solar_collector = 0
        else:
            sun_incidence_angle = math.acos(math.sin(sun_altitude)*math.cos(math.radians(solar_collector_inclination)) + math.cos(sun_altitude)*math.sin(math.radians(solar_collector_inclination))*math.cos(math.radians(sun_azimuth)))
            if math.degrees(sun_incidence_angle)>90:
                sun_incidence_angle = math.radians(90)

            Q_beam_solar_collector = data[i,4] * math.cos(sun_incidence_angle)
            Q_dif_solar_collector = (180 - sun_incidence_angle) / (180) * data[i, 5]


        # OUTPUT -------
        new_row = {'T_exterior': data[i, 0],  # Ambient temperature [ºC]
                   'T_sky': T_sky,  # Sky temperature [ºC]
                   'Q_beam_solar_collector': Q_beam_solar_collector,  # Direct  irradiance on inclined solar collector [W.h/m2]
                   'Q_dif_solar_collector': Q_dif_solar_collector,  # Diffuse irradiance on inclined solar collector [W.h/m2]
                   }
        df_output = df_output.append(new_row, ignore_index=True)



    return df_output

