""""

Info: Computes building surfaces heat losses by radiation to the sky [W/m2].

"""

import math

def building_sky_heat_loss(emissivity,T_surface,T_sky,T_exterior,surface_angle):

    stef_boltzman = 5.67 * 10**(-8)  # [W/m2.K4]

    F_sky = 0.5*(1 + math.cos(surface_angle))  # surface angle in [rad]
    F_ground = 0.5*(1 - math.cos(surface_angle))

    beta = math.sqrt(0.5*(1+math.cos(surface_angle)))

    Q_loss = emissivity * stef_boltzman * ((T_sky+273) ** 4 - (T_surface + 273) ** 4) * F_sky * beta +\
             emissivity * stef_boltzman * ((T_exterior+273) ** 4 - (T_surface + 273) ** 4) * F_sky * (1-beta) + \
             emissivity * stef_boltzman * ((T_exterior+273) ** 4 - (T_surface + 273) ** 4) * F_ground

    return Q_loss