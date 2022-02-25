"""
alisboa/jmcunha


##############################
INFO: Computes power needed for the given flowrate

##############################
INPUT:
        # flowrate  [kg/h]


##############################
OUTPUT:
        # power  [kW]


"""

def flowrate_to_power(flowrate):

    pumping_power_c = 0.0168
    pumping_power_n = 1.1589

    power = pumping_power_c * flowrate ** pumping_power_n  # [kg/h] to [kW]

    return power
