from .h_convection_horizontal import h_convection_horizontal


def steady_state_horizontal_face_up(Q_sun_surface,T_surface_up, T_surface, T_interior, u_surface, Q_rad, area_surface,alpha_surface,
                                       interpolation_weight):

    """Heat balance for the inner vertical surface of the wall

    Parameters
    ----------
    Q_sun_surface : float
        Incident solar radiation [W]

    T_surface_up: float
        Upper surface temperature [ºC]

    T_surface : float
        Surface air temperature [ºC]

    T_interior : float
        Interior air temperature [ºC]

    u_surface : float
        U value [W/m2.K]

    Q_rad : float
        Heat exchanged by radiation [W]

    area_surface

    alpha_surface : float
        Surface absorption []

    interpolation_weight : float

    Returns
    -------
    T_surface_up : float
        Upper surface temperature [ºC]

    """


    h_horizontal = h_convection_horizontal(T_surface_up, T_interior)

    T_surface_up = (Q_sun_surface * alpha_surface / area_surface + Q_rad / area_surface + h_horizontal * T_interior + u_surface * T_surface) / (
                    h_horizontal + u_surface) * (1 - interpolation_weight) + T_surface_up * interpolation_weight



    return T_surface_up
