"""
@author: jmcunha/alisboa

Info: Fluids and materials properties
      Instead of this script - go to SQL/database WITH ALL MATERIALS PROPERTIES

"""


# Fluid/Material Specific Heat kJ/kg.K , T in ºC
def fluid_material_cp(fluid_type,T):

    if fluid_type == "steam": # Steam
        fluid_cp =0.00000017068 * T ** 3 - 0.000028553 * T ** 2 + 0.0047923 * T + 1.6617

    elif fluid_type == "oil": # Thermal Oil
        fluid_cp = 2

    elif fluid_type == "water": # Water
        fluid_cp = 4.18

    elif fluid_type == "flue_gas": # Flue_gas
        fluid_cp = 2.57 * 10 ** (-4) * T + 0.978
        fluid_cp = 2

    else: # Air
        fluid_cp =  1.005
        fluid_cp = 2

    return fluid_cp


def fluid_material_rho(fluid_type):

    if fluid_type == "steam": # Steam
        rho = 1

    elif fluid_type == "oil": # Thermal Oil
        rho = 800

    elif fluid_type == "water": # Water
        rho = 1000

    elif fluid_type == "flue_gas": # Flue_gas
        rho = 1

    else: # Air
        rho =  1.005

    return rho
