""""

Info: Heat Transfer Convection with indoor air. Compute heat [W] exchanged between surfaces and floor's indoor air .

"""

from .....Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical
from .....Sink.characterization.Building.Auxiliary.h_convection_horizontal import h_convection_horizontal

def ht_indoor_air(T_interior,surfaces_horizontal,surfaces_vertical):

    Q_conv = 0

    for surface in surfaces_vertical:
        if surface['area'] != 0:
            h_vertical = h_convection_vertical(surface['temperature'], T_interior)
            Q_conv += (surface['temperature'] - T_interior) * h_vertical * surface['area']

    for surface in surfaces_horizontal:
        if surface['area'] != 0:
            h_horizontal = h_convection_horizontal(surface['temperature'], T_interior)
            Q_conv += (surface['temperature'] - T_interior) * h_horizontal * surface['area']



    return Q_conv