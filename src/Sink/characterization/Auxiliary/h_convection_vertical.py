def h_convection_vertical(T_component_1, T_component_2):
    """Vertical heat transfer coefficient

    ASHRAE Vertical Wall

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

    h_c = 1.31 * delta_T ** (1 / 3)

    return h_c
