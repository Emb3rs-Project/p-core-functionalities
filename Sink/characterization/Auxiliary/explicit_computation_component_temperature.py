def explicit_computation_component_temperature(T_surface, T_surface_in, T_surface_out, u_surface, area_surface,
                                               time_step, c_surface):

    """Explicit equation to compute surface temperature

    Parameters
    ----------
    T_surface : float
        Surface temperature (medium) [ºC]

    T_surface_in : float
        Indoor surface temperature (medium) [ºC]

    T_surface_out : float
        Outer surface temperature (medium) [ºC]

    u_surface : float
        U value surface [W/m2.K]

    area_surface : float
        Surface area [m2]

    time_step : float
        Considered time step [S]

    c_surface : float
        Capacitance surface [J/K]

    Returns
    -------
    T_surface : float

    """

    T_surface = T_surface + (u_surface * (T_surface_in - T_surface) * area_surface + u_surface * (T_surface_out - T_surface)
                             * area_surface) * time_step / c_surface

    return T_surface
