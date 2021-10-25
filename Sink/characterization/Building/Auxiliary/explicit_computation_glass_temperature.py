""""

Info: Explicit equation to compute surface temperature [ºC].

"""


from Sink_Module.Auxiliary.h_convection_vertical import h_convection_vertical

def explicit_computation_glass_temperature (T_glass,T_interior,T_exterior,Q_sun_facade,Q_infra_glass,Q_rad,ratio_glass,area_glass,cp_glass,alpha_glass,u_exterior,time_step):

    h_vertical = h_convection_vertical(T_glass, T_interior)
    T_glass = T_glass + (Q_sun_facade * area_glass * alpha_glass
                         + Q_rad * ratio_glass
                         + Q_infra_glass * area_glass
                         + h_vertical * (T_interior - T_glass) * area_glass
                         + u_exterior * (T_exterior - T_glass) * area_glass) * time_step / cp_glass

    return T_glass