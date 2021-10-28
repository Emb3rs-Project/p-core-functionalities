"""
@author: jmcunha/alisboa

"""

from KB_General.equipment_details import equipment_details
from General.Auxiliary_General.linearize_values import linearize_values

class Add_ORC_Cascaded():

    def __init__(self,orc_cond_temperature_supply,equipment_sub_type,overall_thermal_capacity,electrical_generation,power_fraction):

        # Defined Vars ----
        hx_efficiency = 0.95
        self.object_type = 'equipment'
        self.fuel_type = 'electricity'
        self.equipment_sub_type = equipment_sub_type  # orc/rc

        self.supply_temperature = orc_cond_temperature_supply  # max water temperature
        self.overall_thermal_capacity = overall_thermal_capacity
        self.electrical_generation = electrical_generation  # electrical supply capacity [kW]
        self.supply_capacity = (overall_thermal_capacity - electrical_generation) * hx_efficiency

        # COMPUTE
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
        self.data_teo = {
             'equipment': self.equipment_sub_type,
             'fuel_type': self.fuel_type,
             'max_eletrical_generation': info_max_power['electrical_generation'],  # [kW]
             'max_input_capacity': info_max_power['supply_capacity']/info_max_power['conversion_efficiency'],  # [kW]
             'turnkey_a': turnkey_a,  # [€/kW]
             'turnkey_b': turnkey_b,  # [€]
             'conversion_efficiency': info_max_power['conversion_efficiency'],  # []
             'electrical_conversion_efficiency': info_max_power['electrical_generation']/(info_max_power['supply_capacity']/info_max_power['conversion_efficiency']),
             'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity']/info_max_power['conversion_efficiency']),  # [€/year.kW]
             'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity']/info_max_power['conversion_efficiency']),  # [€/kWh]
             'emissions': 0  # [kg.CO2/kWh]
        }



    def design_equipment(self, power_fraction):

       # Defined vars
       hx_efficiency = 0.95

       overall_thermal_capacity = self.overall_thermal_capacity * power_fraction
       electrical_generation = self.electrical_generation * power_fraction  # electrical supply capacity [kW]
       supply_capacity = (overall_thermal_capacity - electrical_generation) * hx_efficiency  # thermal supply capacity [kW]

       # Turnkey Cost -----
       global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type,electrical_generation)

       # OPEX
       om_var_total = 0

       # Create data for TEO ---
       info = {
           'supply_capacity': supply_capacity,  # [kW]
           'turnkey': turnkey_total,  # [€]
           'om_fix': om_fix_total,  # [€/year]
           'om_var': om_var_total,  # [€]
           'conversion_efficiency': supply_capacity / overall_thermal_capacity,  #
           'electrical_generation': electrical_generation
       }

       return info
