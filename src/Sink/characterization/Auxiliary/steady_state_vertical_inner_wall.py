from .h_convection_vertical import h_convection_vertical


def steady_state_vertical_inner_wall(T_wall_in, T_wall, T_interior, u_wall, Q_rad_inner_facade, area_wall,
                                     interpolation_weight):

    """Heat balance for the inner horizontal surface of the wall

    Parameters
    ----------
    T_wall_in : float
        Inner wall temperature [ºC]

    T_wall : float
        Wall temperature [ºC]

    T_interior : float
        Interior air temperature [ºC]

    u_wall : float
        Wall value [W/m2.K]

    Q_rad_inner_facade : float
        Heat exchanged by radiation [W]

    area_wall : float
        Wall area [m2]

    interpolation_weight : float


    Returns
    -------
    T_wall_in : float
            Inner wall temperature [ºC]


    """

    h_vertical = h_convection_vertical(T_wall_in, T_interior)

    T_wall_in = (Q_rad_inner_facade / area_wall
                 + h_vertical * T_interior
                 + u_wall * T_wall) / (h_vertical + u_wall) * (1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in
