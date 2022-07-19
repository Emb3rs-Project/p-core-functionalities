def ht_radiation_equation(emissivity, area_1, T_component_1, T_component_2, F_1_2):
    """Compute heat transfer, by radiation, between surfaces and indoor air

    Parameters
    ----------
    emissivity : float
        Surface emissivity []

    area_1 : float
        Area [m2]

    T_component_1 : float
        Component temperature [ºC]

    T_component_2 : float
            Component temperature [ºC]

    F_1_2 : float
        View factor []

    Returns
    -------
    Q_radiation : float
        Exchanged heat by radiation [W]

    """

    stef_Boltzmann = 5.67 * 10 ** (-8)  # [W/m2.K4]

    Q_radiation = emissivity * stef_Boltzmann * area_1 * (
                (T_component_2 + 273) ** 4 - (T_component_1 + 273) ** 4) * F_1_2  # [W]

    return Q_radiation
