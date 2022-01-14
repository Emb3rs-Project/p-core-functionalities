"""
alisboa/jmcunha


##############################
INFO: compute electric chiller COP and heat pump ERR according to given temperatures


##############################
INPUT:
        # type - equipment type, e.g. electric_chiller or heat pump
        # hot_temperature  [ºC]
        # cold_temperature [ºC]


##############################
RETURN:
        # cop or err  []


"""


def compute_cop_err(type, hot_temperature, cold_temperature,evaporator_temperature=15):

    # evaporator_temperature = 15  # defined ambient temperature [ºC]

    if type == 'electric_chiller':
        cop = 0.405 * (cold_temperature + 273 + 5) / (evaporator_temperature - cold_temperature + 10)
        return cop

    else:
        err = 0.55 * (hot_temperature + 273 + 5) / (hot_temperature - evaporator_temperature + 10)
        return err
