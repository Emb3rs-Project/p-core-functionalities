"""
@author: jmcunha/alisboa

Info: Determining the flowrate of the supply and excess supply heat/cold stream  [kg/h].
      Input: capacity [kW]; temperatures [ºC]
"""

from ...KB_General.fluid_material import fluid_material_cp

def compute_flow_rate(fluid,capacity,supply_temperature,return_temperature):

    if supply_temperature == return_temperature:
        supply_flowrate = 0
    else:
        fluid_cp = fluid_material_cp(fluid, supply_temperature)
        supply_flowrate = capacity / abs(fluid_cp * (supply_temperature - return_temperature)) * 3600

    return supply_flowrate