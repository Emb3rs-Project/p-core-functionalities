import math


def surface_outside_rad_heat_loss(emissivity_surface, T_surface, T_sky, T_exterior, surface_angle):
    """Computes building surface's heat losses by radiation to the sky

    Parameters
    ----------
    emissivity_surface : float
        Surface emissivity []

    T_surface : float
        Surface temperature [ºC]

    T_sky : float
        Sky temperature [ºC]

    T_exterior : float
        Ambient temperature [ºC]

    surface_angle : float
        Surface angle [º]


    Returns
    -------
    Q_loss : float
        Heat lost by radiation [W/m2]

    """

    stef_Boltzmann = 5.67 * 10**(-8)  # [W/m2.K4]

    # view factors
    F_sky = 0.5*(1 + math.cos(surface_angle))
    F_ground = 0.5*(1 - math.cos(surface_angle))

    beta = math.sqrt(0.5*(1+math.cos(surface_angle)))

    Q_loss = emissivity_surface * stef_Boltzmann * ((T_sky+273) ** 4 - (T_surface + 273) ** 4) * F_sky * beta +\
             emissivity_surface * stef_Boltzmann * ((T_exterior+273) ** 4 - (T_surface + 273) ** 4) * F_sky * (1-beta) + \
             emissivity_surface * stef_Boltzmann * ((T_exterior+273) ** 4 - (T_surface + 273) ** 4) * F_ground

    return Q_loss