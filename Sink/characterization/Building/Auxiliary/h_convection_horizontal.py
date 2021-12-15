"""
alisboa/jmcunha


##############################
INFO: Horizontal heat transfer coefficient (Walton Unstable Horizontal Or Tilt).


##############################
INPUT:
        # T_component_1  [ºC]
        # T_component_2  [ºC]


##############################
OUTPUT:
        # h_c  [W/m2.K]


"""


def h_convection_horizontal(T_component_1, T_component_2):

    delta_T = abs(T_component_1 - T_component_2)

    h_c = 9.482 * delta_T ** (1 / 3) / 7.283  # [W/m2.K]

    return h_c
