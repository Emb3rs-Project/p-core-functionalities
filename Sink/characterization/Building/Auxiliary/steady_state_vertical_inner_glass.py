"""
alisboa/jmcunha


##############################
INFO: Heat balance for the inner horizontal surface of the glass.


##############################
INPUT:
        # T_glass_in  [ºC]
        # T_glass  [ºC]
        # T_interior  [ºC]
        # u_glass  [W/m2.K]
        # Q_rad_inner_facade  [W]
        # ratio_glass  []
        # area_glass  [m2]
        # interpolation_weight  []


##############################
OUTPUT:
        # T_glass_in  [ºC]


"""

from .....Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical


def steady_state_vertical_inner_glass(Q_sun, alpha_glass, T_glass_in, T_glass_out, T_interior, u_glass, Q_rad, area_glass,
                                     interpolation_weight):

    h_vertical = h_convection_vertical(T_glass_in, T_interior)

    T_glass_in = (Q_sun * alpha_glass + Q_rad / area_glass
                 + h_vertical * T_interior
                 + u_glass * T_glass_out) / (h_vertical + u_glass) * (1 - interpolation_weight) + T_glass_in * interpolation_weight

    return T_glass_in
