"""
alisboa/jmcunha


##############################
INFO: compute electric chiller COP and heat pump ERR according to given temperatures


##############################
INPUT:
        # type - equipment type, e.g. electric_chiller or heat pump
        # condenser_temperature  [ºC]
        # cold_temperature [ºC]


##############################
RETURN:
        # cop or err  []


"""


def compute_cop_err(type, condenser_temperature=2,evaporator_temperature=15):

    if type == 'compression_chiller':
        cop = 0.405 * (condenser_temperature + 273 + 5) / (evaporator_temperature - condenser_temperature + 10)
        return cop

    else:
        err = 0.55 * (condenser_temperature + 273 + 5) / (condenser_temperature - evaporator_temperature + 10)
        return err
