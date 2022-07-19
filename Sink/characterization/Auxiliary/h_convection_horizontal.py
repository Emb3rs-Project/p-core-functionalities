def h_convection_horizontal(T_component_1, T_component_2):
    """ Horizontal heat transfer coefficient

    Walton Unstable Horizontal Or Tilt

    Parameters
    ----------
    T_component_1 : float,
        Component temperature [ºC]

    T_component_2 : float,
        Component temperature [ºC]

    Returns
    -------
    h_c : float
        Convection coefficient [W/m2.K]
    """

    delta_T = abs(T_component_1 - T_component_2)

    h_c = 9.482 * delta_T ** (1 / 3) / 7.283  # [W/m2.K]

    return h_c
