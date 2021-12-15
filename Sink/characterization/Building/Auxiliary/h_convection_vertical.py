"""
alisboa/jmcunha


##############################
INFO: Vertical heat transfer coefficient (ASHRAE Vertical Wall).


##############################
INPUT:
        # T_component_1  [ºC]
        # T_component_2  [ºC]


##############################
OUTPUT:
        # h_c  [W/m2.K]


"""


def h_convection_vertical(T_component_1, T_component_2):

    delta_T = abs(T_component_1 - T_component_2)

    h_c = 1.31 * delta_T ** (1 / 3)

    return h_c
