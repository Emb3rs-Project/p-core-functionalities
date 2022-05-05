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


def steady_state_horizontal_face_up(Q_sun_surface,T_surface_up, T_surface, T_interior, u_surface, Q_rad, area_surface,alpha_surface,
                                       interpolation_weight):


    h_horizontal = h_convection_horizontal(T_surface_up, T_interior)

    T_surface_up = (Q_sun_surface * alpha_surface / area_surface + Q_rad / area_surface + h_horizontal * T_interior + u_surface * T_surface) / (
                    h_horizontal + u_surface) * (1 - interpolation_weight) + T_surface_up * interpolation_weight



    return T_surface_up
