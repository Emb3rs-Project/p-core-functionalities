""""

Info: Heat Transfer Radiation between horizontal surfaces and remaining.
Compute heat [W] exchanged between horizontal surface and remaining ones.

"""
from Sink.characterization.Building.Auxiliary.ht_radiation_equation import ht_radiation_equation

def ht_radiation_horizontal_surface(surface_analysed, surface_1, surface_2, surface_3, surface_4, surface_5, surface_6,surface_7, surface_8,surface_9):

    emissivity_wall = 0.9
    emissivity_glass = 0.85

    Q_rad = 0

    surfaces = [surface_1, surface_2, surface_3, surface_4, surface_5, surface_6, surface_7, surface_8,surface_9]

    total_area_seen = 0
    for surface in surfaces:
        total_area_seen += surface['area']

    # Surface analysed
    emissivity_vertical_surface = emissivity_wall

    # Other Surface
    for surface in surfaces:
        if surface['type'] == 'glass':
            emissivity_remaining_surface = emissivity_glass
        else:
            emissivity_remaining_surface = emissivity_wall

        effective_emissivity = (1 / emissivity_vertical_surface + 1 / emissivity_remaining_surface - 1) ** (-1)

        if surface['area'] != 0:
            F = surface['area'] / total_area_seen
            Q_rad += ht_radiation_equation(effective_emissivity, surface_analysed['area'],
                                           surface_analysed['temperature'], surface['temperature'], F)  # [W]

    return Q_rad