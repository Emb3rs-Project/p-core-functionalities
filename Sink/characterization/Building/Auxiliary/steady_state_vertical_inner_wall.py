"""
alisboa/jmcunha


##############################
INFO: Heat balance for the inner horizontal surface of the wall.


##############################
INPUT:
        # T_wall_in  [ºC]
        # T_wall  [ºC]
        # T_interior  [ºC]
        # u_wall  [W/m2.K]
        # Q_rad_inner_facade  [W]
        # ratio_wall  []
        # area_wall  [m2]
        # interpolation_weight  []


##############################
OUTPUT:
        # T_wall_in  [ºC]


"""

from .....Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical


def steady_state_vertical_inner_wall(T_wall_in, T_wall, T_interior, u_wall, Q_rad_inner_facade, area_wall,
                                     interpolation_weight):

    h_vertical = h_convection_vertical(T_wall_in, T_interior)

    T_wall_in = (Q_rad_inner_facade / area_wall
                 + h_vertical * T_interior
                 + u_wall * T_wall) / (h_vertical + u_wall) * (1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in
