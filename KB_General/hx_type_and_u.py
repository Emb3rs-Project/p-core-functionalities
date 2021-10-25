"""
@author: jmcunha/alisboa

Info: Receive Fluid type and return appropriate heat exchanger and U value [W/m2.K]

Return: [hx_type,hx_u_value]
"""


def hx_type_and_u(fluid_1,fluid_2):

    # Connect with KB_General, get oil - liquid, water -liquid, steam - steam, air - gas, fluegas - gas ...
    if (fluid_1 == 'liquid' or fluid_1 == 'water' or fluid_1 == 'oil') and (fluid_2 == 'liquid' or fluid_2 == 'water' or fluid_2 == 'oil'):
        hx_type = 'hx_plate'
        hx_u_value = 2000

    elif (fluid_1 == 'flue_gas' and fluid_2 == 'oil') or (fluid_1 == 'oil' and fluid_2 == 'flue_gas'):
        hx_type = 'hx_gas_cooler'
        hx_u_value = 50 # not interesting

    elif (fluid_1 == 'oil' and fluid_2 == 'steam') :
        hx_type = 'kettle_boiler'
        hx_u_value = 800 # not interesting


    elif (fluid_1 == 'steam' and fluid_2 == 'water') or (fluid_1 == 'liquid' and fluid_2 == 'water'):
        hx_type = 'hx_shell_tubes'
        hx_u_value = 800

    else:
        print('def:hx_type_u')
        hx_type = 'error'
        hx_u_value = 0
        hx_type = 'hx_plate'
        hx_u_value = 800

    return hx_type,hx_u_value