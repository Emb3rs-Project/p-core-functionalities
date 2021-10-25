""""

Info: Heat balance for the exterior of the wall.

"""


def steady_state_exterior_wall(T_wall_out,T_wall,T_exterior,u_wall,Q_sun,Q_infra_wall,alpha_wall,u_exterior,interpolation_weight):

    T_wall_out = (Q_sun * alpha_wall
                  + Q_infra_wall
                  + u_exterior * T_exterior
                  + u_wall * T_wall) \
                   / (u_exterior + u_wall) * (1 - interpolation_weight) + T_wall_out * interpolation_weight

    return T_wall_out