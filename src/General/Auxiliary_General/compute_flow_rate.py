"""
alisboa/jmcunha


##############################
INFO: Compute flow rate

##############################
INPUT:
        # fluid  - fluid type
        # capacity  [kW]
        # supply_temperature  [ºC]
        # return_temperature  [ºC]

##############################
RETURN:
        # supply_flowrate  [kg/h]


"""
from ...utilities.kb import KB
from ...KB_General.medium import Medium

def compute_flow_rate(kb: KB, fluid,capacity,supply_temperature,return_temperature):
    """ Compute mass flow rate

    Parameters
    ----------
    kb : dict
        Knowledge Base data

    fluid : str
        Fluid name

    capacity :
        Stream capacity [kW]

    supply_temperature :
        Stream supply temperature [ºC]

    return_temperature :
        Stream return temperature [ºC]

    Returns
    -------
    supply_flowrate : float
        Stream mass flowrate [kg/h]

    """


    if supply_temperature == return_temperature:
        supply_flowrate = 0
    else:
        medium = Medium(kb)
        fluid_cp = medium.cp(fluid, supply_temperature)
        supply_flowrate = capacity / abs(fluid_cp * (supply_temperature - return_temperature)) * 3600  # [kg/h]

    return supply_flowrate