"""
alisboa/jmcunha


##############################
INFO: Compute heat transfer, by radiation, between surfaces and indoor air.


##############################
INPUT:
        # emissivity  []
        # area_1  [m2]
        # T_component_1  [ºC]
        # T_component_2  [ºC]
        # F_1_2 - view factor []

        Where in each surface of horizontal_surfaces/vertical_surfaces, the following keys:
            # temperature  [ºC]
            # area  [m2]
            # type - e.g. 'wall' or 'glass'

##############################
OUTPUT:
        # Q_convection  [W]


"""


def ht_radiation_equation(emissivity, area_1, T_component_1, T_component_2, F_1_2):

    stef_Boltzmann = 5.67 * 10 ** (-8)  # [W/m2.K4]

    Q_radiation = emissivity * stef_Boltzmann * area_1 * (
                (T_component_2 + 273) ** 4 - (T_component_1 + 273) ** 4) * F_1_2  # [W]

    return Q_radiation
