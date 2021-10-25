""""

Info: Heat balance for the interior horizontal surfaces.

"""


from Sink.characterization.Building.Auxiliary.h_convection_vertical import h_convection_vertical


def steady_state_vertical_inner_wall(T_wall_in,T_wall,T_interior,u_wall,Q_rad_inner_facade,ratio_wall,area_wall,interpolation_weight):

    h_vertical = h_convection_vertical(T_wall_in, T_interior)


    T_wall_in = (Q_rad_inner_facade * ratio_wall / area_wall
                 + h_vertical * T_interior
                 + u_wall * T_wall) / (h_vertical + u_wall) * (1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in