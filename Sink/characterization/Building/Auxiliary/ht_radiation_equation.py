""""

Info: Heat Transfer Radiation Equation. Compute heat [W] exchanged between surfaces by radiation.

"""

def ht_radiation_equation(emissivity,area_1,T_1,T_2,F_1_2):

    stef_boltzman = 5.67 * 10**(-8)  # [W/m2.K4]

    Q_rad = emissivity * stef_boltzman * area_1 * ((T_2+273)**4 - (T_1+273)**4) * F_1_2  # [W]

    return Q_rad