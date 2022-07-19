def steady_state_exterior_wall(T_wall_out, T_wall, T_exterior, u_wall, Q_sun, Q_infra_wall, alpha_wall, u_exterior,
                               interpolation_weight):
    """Heat balance for the outer surface of the wall

    Parameters
    ----------
    T_wall_out : float
        Outer wall temperature [ºC]

    T_wall : float
        Wall temperature [ºC]

    T_exterior : float
        Ambient temperature [ºC]

    u_wall : float
        Wall U value [W/m2.K]

    Q_sun : float
        Incident solar radiation [W]

    Q_infra_wall : float
        Sky radiation heat losses [W]

    alpha_wall : float
        Wall absorption []

    u_exterior : float
        Exterior U value [W/m2.K]

    interpolation_weight : float


    Returns
    -------
    T_wall_out : float
        Outer wall temperature

    """
    T_wall_out = (Q_sun * alpha_wall
                  + Q_infra_wall
                  + u_exterior * T_exterior
                  + u_wall * T_wall) \
                 / (u_exterior + u_wall) * (1 - interpolation_weight) + T_wall_out * interpolation_weight

    return T_wall_out
