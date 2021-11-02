""""

Info: Heat balance for the interior of the wall.

"""


from .....Sink.characterization.Building.Auxiliary.h_convection_horizontal import h_convection_horizontal


def steady_state_horizontal_inner_wall(T_wall_in,T_wall,T_interior,u_wall,Q_rad_facade,ratio_wall,area_wall,interpolation_weight):

    h_horizontal = h_convection_horizontal(T_wall_in, T_interior)

    T_wall_in = (Q_rad_facade * ratio_wall / area_wall
                 + h_horizontal * T_interior
                 + u_wall * T_wall) / (h_horizontal + u_wall) * (1 - interpolation_weight) + T_wall_in * interpolation_weight

    return T_wall_in