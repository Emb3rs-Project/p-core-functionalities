from .ht_radiation_equation import ht_radiation_equation


def ht_radiation_horizontal_surface(surface_analysed, surface_1, surface_2, surface_3, surface_4, surface_5, surface_6,
                                    surface_7, surface_8, surface_9, emissivity_wall, emissivity_glass):

    """Compute heat transfer, by radiation, between horizontal (roof, floor, deck_above ad deck_below) and remaining surfaces

    Parameters
    ----------
    surface_analysed : dict
        Surface data; Where in each surface, the following keys:

            - temperature
                Surface temperature[ºC]

            - area
                Surface area [m2]

            - type
                Surface type; e.g. 'wall' or 'glass'

    surface_1 : dict

    surface_2 : dict

    surface_3 : dict

    surface_4 : dict

    surface_5 : dict

    surface_6 : dict

    surface_7 : dict

    surface_8 : dict

    surface_9 : dict

    emissivity_wall : float
        Wall emissivity

    emissivity_glass : float
        Glass emissivity

    Returns
    -------
    Q_radiation : float
        Exchanged heat by radiation [W]

    """

    Q_radiation = 0

    surfaces = [surface_1, surface_2, surface_3, surface_4, surface_5, surface_6, surface_7, surface_8, surface_9]

    total_area_seen = 0
    for surface in surfaces:
        total_area_seen += surface['area']

    # Surface analysed
    emissivity_horizontal_surface = emissivity_wall

    # Other Surface
    for surface in surfaces:
        if surface['type'] == 'glass':
            emissivity_remaining_surface = emissivity_glass
        else:
            emissivity_remaining_surface = emissivity_wall

        effective_emissivity = (1 / emissivity_horizontal_surface + 1 / emissivity_remaining_surface - 1) ** (-1)

        if surface['area'] != 0:
            F = surface['area'] / total_area_seen
            Q_radiation += ht_radiation_equation(effective_emissivity, surface_analysed['area'],surface_analysed['temperature'],
                                                 surface['temperature'], F)  # [W]

    return Q_radiation
