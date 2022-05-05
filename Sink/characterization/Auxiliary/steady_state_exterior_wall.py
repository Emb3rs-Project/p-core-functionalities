"""
alisboa/jmcunha


##############################
INFO: Heat balance for the outer surface of the wall.


##############################
INPUT:
        # T_wall_out  [ºC]
        # T_wall  [ºC]
        # T_exterior  [ºC]
        # u_wall  [W/m2.K]
        # Q_sun  [W]
        # Q_infra_wall  [W]
        # alpha_wall  []
        # u_exterior  [W/m2.K]
        # interpolation_weight  []


##############################
OUTPUT:
        # T_wall_out  [ºC]


"""


def steady_state_exterior_wall(T_wall_out, T_wall, T_exterior, u_wall, Q_sun, Q_infra_wall, alpha_wall, u_exterior,
                               interpolation_weight):

    T_wall_out = (Q_sun * alpha_wall
                  + Q_infra_wall
                  + u_exterior * T_exterior
                  + u_wall * T_wall) \
                 / (u_exterior + u_wall) * (1 - interpolation_weight) + T_wall_out * interpolation_weight

    return T_wall_out
