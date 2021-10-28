"""
@author: jmcunha/alisboa

"""

from KB_General.equipment_details import equipment_details
from KB_General.fuel_properties import fuel_properties
from General.Auxiliary_General.linearize_values import linearize_values


class Add_CHP():

    def __init__(self, fuel_type, country,consumer_type,supply_capacity,power_fraction,supply_temperature,return_temperature):

        # Defined Vars ----
        self.object_type = 'equipment'

        if supply_temperature < 100:
            self.equipment_sub_type = 'chp_gas_engine'
        else:
            self.equipment_sub_type = 'chp_gas_turbine'

        self.fuel_type = fuel_type
        self.fuel_properties = fuel_properties(country,self.fuel_type,consumer_type)


        # COMPUTE -----
        self.supply_temperature = supply_temperature   # equipment directly supplies grid
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity  # equipment directly supplies grid
        all_conversion_efficiency, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type, supply_capacity)
        self.thermal_conversion_efficiency = all_conversion_efficiency[0]
        self.electrical_conversion_efficiency = all_conversion_efficiency[1]

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
            'max_supply_capacity': info_max_power['supply_capacity'] / self.thermal_conversion_efficiency,  # [kW]
            'electrical_generation': info_max_power['electrical_generation'],
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.thermal_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] / self.thermal_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / self.thermal_conversion_efficiency),  # [€/kWh]
            'emissions': self.fuel_properties['CO2_emission'] / self.thermal_conversion_efficiency  # [kg.CO2/kWh]

        }


    def design_equipment(self,power_fraction):

        # COMPUTE ----
        supply_capacity = self.supply_capacity * (power_fraction)  # thermal power needed [kWh]
        electrical_generation = supply_capacity/(self.thermal_conversion_efficiency)*(self.electrical_conversion_efficiency)  # [kW]

        # Cost -----
        all_conversion_efficiency, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type, supply_capacity)
        fuel_power_equipment = supply_capacity / self.thermal_conversion_efficiency
        om_var_total = self.fuel_properties['price'] * fuel_power_equipment

        # Create data for TEO ---
        info = {
            'electrical_generation': electrical_generation,
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # # [€/year]
            'om_var': om_var_total  # [€]
            }

        return info









