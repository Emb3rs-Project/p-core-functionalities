from .h_convection_vertical import h_convection_vertical


def steady_state_vertical_inner_glass(Q_sun, alpha_glass, T_glass_in, T_glass_out, T_interior, u_glass, Q_rad, area_glass,
                                     interpolation_weight):

    """Heat balance for the inner horizontal surface of the glass

    Parameters
    ----------
    Q_sun : float
        Incident solar radiation [W]

    alpha_glass : float
        Absorption coefficient []

    T_glass_in : float
        Inner glass temperature [ºC]

    T_glass_out : float
        Outer glass temperature [ºC]

    T_interior : float
        Interior air temperature [ºC]

    u_glass : float
        Glass U value [W/m2.K]

    Q_rad : float
        Heat exchanged by radiation [W]

    area_glass: float
        Glass area [m2]

    interpolation_weight : float


    Returns
    -------
    T_glass_in : float
        Inner glass temperature [ºC]

    """

    h_vertical = h_convection_vertical(T_glass_in, T_interior)

    T_glass_in = (Q_sun * alpha_glass + Q_rad / area_glass
                 + h_vertical * T_interior
                 + u_glass * T_glass_out) / (h_vertical + u_glass) * (1 - interpolation_weight) + T_glass_in * interpolation_weight

    return T_glass_in
