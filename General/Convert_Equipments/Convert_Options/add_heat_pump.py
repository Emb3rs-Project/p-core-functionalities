"""
@author: jmcunha/alisboa

"""

from ....KB_General.equipment_details import equipment_details
from ....KB_General.fuel_properties import fuel_properties
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....General.Auxiliary_General.compute_cop_err import compute_cop_err


class Add_Heat_Pump():

    def __init__(self,country, consumer_type, supply_capacity,power_fraction,supply_temperature,return_temperature):

        # Defined Vars ----
        self.object_type = 'equipment'
        self.equipment_sub_type = 'heat_pump'
        self.fuel_type = 'electricity'
        self.fuel_properties = fuel_properties(country,self.fuel_type,consumer_type)

        # COMPUTE -----
        self.supply_temperature = supply_temperature  # equipment directly supplies grid
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity  # Heat supply capacity [kW]
        self.global_conversion_efficiency = compute_cop_err(self.equipment_sub_type,self.supply_temperature,self.return_temperature)  # COP/ERR

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
            'fuel_type':self.fuel_type,
            'max_input_capacity': info_max_power['supply_capacity'] / self.global_conversion_efficiency,  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] / self.global_conversion_efficiency  # [kg.CO2/kWh]

            }

    def design_equipment(self,power_fraction):

        # COMPUTE ----
        supply_capacity = self.supply_capacity * power_fraction  # thermal power needed [kW]
        eletric_power_equipment = supply_capacity/self.global_conversion_efficiency

        # Cost -----
        global_conversion_efficiency_equipment, om_fix_total, turnkey_equipment = equipment_details(self.equipment_sub_type, supply_capacity)
        om_var_total = self.fuel_properties['price'] * eletric_power_equipment

        # Create data for TEO ---
        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_equipment,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info











