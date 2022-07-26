from .h_convection_horizontal import h_convection_horizontal


def steady_state_horizontal_face_down(T_wall_in, T_wall, T_interior, u_wall, Q_rad, area_wall,
                                       interpolation_weight):

    """Heat balance for the inner vertical surface of the wall

    Parameters
    ----------
    T_wall_in : float
        Inner wall temperature [ºC]

    T_wall : float
        Wall temperature [ºC]

    T_interior : float
        Interior air temperature [ºC]

    u_wall : float
        Wall U value [W/m2.K]

    Q_rad : float
        Heat exchanged by radiation [W]

    area_wall : float
        Wall area [m2]

    interpolation_weight : float

    Returns
    -------
    T_wall_in : float
        Inner wall temperature [ºC]

    """

    h_horizontal = h_convection_horizontal(T_wall_in, T_interior)

    T_wall_in = (Q_rad / area_wall
                 + h_horizontal * T_interior
                 + u_wall * T_wall) / (h_horizontal + u_wall) * (
                        1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in
