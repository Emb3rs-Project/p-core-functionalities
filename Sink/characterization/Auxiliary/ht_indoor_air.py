from .h_convection_vertical import h_convection_vertical
from .h_convection_horizontal import h_convection_horizontal


def ht_indoor_air(T_interior, horizontal_surfaces, vertical_surfaces):
    """Compute heat transfer, by convection, between all surfaces and indoor air.

    Parameters
    ----------
    T_interior : float
        Indoor air temperature [ºC]

    horizontal_surfaces : list with dicts
        Every surface temperature and area data; Where in each surface of horizontal_surfaces/vertical_surfaces, the following keys:

            - temperature : float
                [ºC]

            - area : float
                [m2]

    vertical_surfaces : list


    Returns
    -------
    Q_convection : float
        Exchanged heat by convection [W]

    """

    Q_convection = 0

    for surface in vertical_surfaces:
        if surface['area'] != 0:
            h_vertical = h_convection_vertical(surface['temperature'], T_interior)
            Q_convection += (surface['temperature'] - T_interior) * h_vertical * surface['area']

    for surface in horizontal_surfaces:
        if surface['area'] != 0:
            h_horizontal = h_convection_horizontal(surface['temperature'], T_interior)
            Q_convection += (surface['temperature'] - T_interior) * h_horizontal * surface['area']

    return Q_convection
