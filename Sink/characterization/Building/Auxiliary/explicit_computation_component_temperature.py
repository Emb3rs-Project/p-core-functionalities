"""
alisboa/jmcunha


##############################
INFO: Explicit equation to compute surface temperature.


##############################
INPUT:
        # T_surface  [ºC]
        # T_surface_in  [ºC]
        # T_surface_out  [ºC]
        # u_surface  [W/m2.K]
        # area_surface  [m2]
        # time_step  [s]
        # c_surface  [


##############################
OUTPUT:
        # T_surface  [ºC]


"""


def explicit_computation_component_temperature(T_surface, T_surface_in, T_surface_out, u_surface, area_surface,
                                               time_step, c_surface):

    T_surface = T_surface + (u_surface * (T_surface_in - T_surface) * area_surface + u_surface * (T_surface_out - T_surface)
                             * area_surface) * time_step / c_surface

    return T_surface
