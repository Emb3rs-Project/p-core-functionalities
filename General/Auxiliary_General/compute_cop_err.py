"""
INFO: Compute Electric Chiller COP according to temperatures.

"""

def compute_cop_err(type,hot_temperature, cold_temperature):

    T_amb = 15  # defined ambient temperature [ºC]

    if type == 'electric_chiller':
        cop = 0.405 * (cold_temperature+273+5)/(T_amb - cold_temperature + 10)
    else:
        cop = 0.55 * (hot_temperature + 273 + 5) / (hot_temperature - T_amb + 10)

    return cop