""""

Info: Vertical heat transfer coefficient [W/m2.K].

"""
def h_convection_vertical (T_1,T_2):

    delta_T = abs(T_1-T_2)

    h = 1.31 * delta_T**(1/3) # [W/m2.K] - ref:https://bigladdersoftware.com/epx/docs/8-4/engineering-reference/inside-heat-balance.html#inside-heat-balance

    return h