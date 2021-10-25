""""

Info: Explicit equation to compute surface temperature [ºC].

"""

def explicit_computation_component_temperature (T_surface,T_surface_in,T_surface_out,u_surface,area_surface,time_step,c_surface):

    T_surface = T_surface + (u_surface * (T_surface_in - T_surface) * area_surface + u_surface * (T_surface_out - T_surface) * area_surface) * time_step / c_surface

    return T_surface