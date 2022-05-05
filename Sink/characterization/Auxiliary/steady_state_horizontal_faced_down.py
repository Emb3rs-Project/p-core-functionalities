"""
alisboa/jmcunha


##############################
INFO: Heat balance for the inner vertical surface of the wall.


##############################
INPUT:
        # T_wall_in  [ºC]
        # T_wall  [ºC]
        # T_interior  [ºC]
        # u_wall  [W/m2.K]
        # Q_rad_facade  [W]
        # ratio_wall  []
        # area_wall  [m2]
        # interpolation_weight  []


##############################
OUTPUT:
        # T_wall_in  [ºC]


"""

from .h_convection_horizontal import h_convection_horizontal


def steady_state_horizontal_face_down(T_wall_in, T_wall, T_interior, u_wall, Q_rad, area_wall,
                                       interpolation_weight):

    h_horizontal = h_convection_horizontal(T_wall_in, T_interior)

    T_wall_in = (Q_rad / area_wall
                 + h_horizontal * T_interior
                 + u_wall * T_wall) / (h_horizontal + u_wall) * (
                        1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in
