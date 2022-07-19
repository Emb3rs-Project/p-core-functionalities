# default values for compression chiller
def compute_cop_eer(type, condenser_temperature=45,evaporator_temperature=2):
    """Compute electric chiller COP and heat pump ERR according to given temperatures

    Parameters
    ----------
    type :
        Equipment type, e.g. electric_chiller or heat pump

    condenser_temperature :
        Condenser temperature [ºC]

    evaporator_temperature :
        Evaporator temperature [ºC]


    Returns
    -------
    cop/err : float
        Cop/Err of chiller/heat pump []

    """

    if type == 'compression_chiller':
        cop = 0.405 * (condenser_temperature + 273) / (condenser_temperature - evaporator_temperature)
        return cop

    else:
        err = 0.55 * (condenser_temperature + 273) / (condenser_temperature - evaporator_temperature)
        return err
