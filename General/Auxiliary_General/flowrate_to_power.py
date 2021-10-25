"""
INFO: Pumping - [m3/h] to [kW]  from KB_General

INPUT: Flowrate in [kg/h]

OUTPUT: Power in [kW]

"""

def flowrate_to_power(flowrate):

    return 0.0168 * (flowrate/ 1000) ** (1.15) * 10**(-3) # [m3/h] to [kW]  from KB_General


