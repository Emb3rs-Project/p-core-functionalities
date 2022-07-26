def flowrate_to_power(flowrate):
    """ Computes power needed for a given mass flowrate

    Parameters
    ----------
    flowrate : float
        Mass flowrate [kg/h]

    Returns
    -------
    power : float
        Power [kW]


    """

    pumping_power_c = 0.0168
    pumping_power_n = 1.1589

    power = pumping_power_c * flowrate ** pumping_power_n  # [kg/h] to [kW]

    return power
