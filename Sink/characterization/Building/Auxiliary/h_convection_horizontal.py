""""

Info: Horizontal heat transfer coefficient [W/m2.K].

"""


def h_convection_horizontal(T_1,T_2):

    delta_T = abs(T_1 - T_2)

    h = 9.482*delta_T**(1/3) / 7.283  # [W/m2.K]

    return h