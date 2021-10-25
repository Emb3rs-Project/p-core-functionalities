
"""
@author: jmcunha/alisboa

"""

from KB_General.equipment_details import equipment_details
from KB_General.fuel_properties import fuel_properties
from General.Auxiliary_General.linearize_values import linearize_values


class Add_Absorption_Chiller():

    def __init__(self,country,consumer_type,supply_capacity ,power_fraction):

        # Defined Vars ----
        self.object_type = 'equipment'
        self.equipment_sub_type = 'thermal_chiller'
        self.fuel_type = 'electricity'
        self.thermal_chiller_evap_T_cold = 70
        self.thermal_chiller_evap_T_hot = 90
        self.country = country
        self.fuel_properties = fuel_properties(country,self.fuel_type,consumer_type)
        self.supply_temperature = 7  # equipment directly supplies [ºC]
        self.return_temperature = 12  # [ºC]

        # COMPUTE -----
        self.supply_capacity = supply_capacity  # equipment directly supplies grid
        # get only thermal chiller COP
        self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type, self.supply_capacity)  # [€]

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(power_fraction=1)
        # Power Fraction
        info_power_fraction = self.design_equipment(power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'],
                                                info_power_fraction['supply_capacity']
                                                )

        self.data_teo = \
            {
            'equipment': self.equipment_sub_type,
            'max_supply_capacity': info_max_power['supply_capacity'] / self.global_conversion_efficiency,  # [kW]
            'electrical_generation': info_max_power['electrical_generation'],
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (
                        info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency), # [€/kWh]
            'emissions': self.fuel_properties['CO2_emission'] / self.global_conversion_efficiency  # [kg.CO2/kWh]

            }

    def design_equipment(self, power_fraction):

        # COMPUTE ----
        # Design Absorption Chiller
        supply_capacity = self.supply_capacity * (power_fraction)   # thermal power needed [kWh]

        # Turnkey Cost -----
        global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type, supply_capacity)  # [€]

        # OPEX Cost -----
        eletric_power_equipment = supply_capacity / self.global_conversion_efficiency
        om_var_total = self.fuel_properties['price'] * eletric_power_equipment


        # Create data for TEO ---
        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info










