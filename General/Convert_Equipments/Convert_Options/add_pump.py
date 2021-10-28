"""
@author: jmcunha/alisboa

"""

from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from KB_General.equipment_details import equipment_details
from KB_General.fuel_properties import fuel_properties
from General.Auxiliary_General.flowrate_to_power import flowrate_to_power
from General.Auxiliary_General.linearize_values import linearize_values
from KB_General.fluid_material import fluid_material_rho

class Add_Pump():

    def __init__(self, country, consumer_type, fluid, supply_capacity, power_fraction, supply_temperature, return_temperature):

        # Defined Vars ----
        self.object_type = 'equipment'
        self.equipment_sub_type = 'circulation_pumping'
        self.fuel_type = 'electricity'
        self.fuel_properties = fuel_properties(country,self.fuel_type,consumer_type)

        # COMPUTE -----
        # Equipment Temperatures
        self.fluid = fluid
        self.supply_temperature = supply_temperature
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity

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
            'fuel_tyoe': self.fuel_type,
            'max_supply_capacity': info_max_power['supply_capacity'] ,  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': 1,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] ),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] ),  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] / self.global_conversion_efficiency  # [kg.CO2/kWh]
            }

    def design_equipment(self, power_fraction):
        # Fluid and Fuel cost
        fluid_rho = fluid_material_rho(self.fluid,(self.supply_temperature+self.return_temperature)/2)

        # Flowrate
        supply_capacity = self.supply_capacity * power_fraction  # thermal power needed [kWh]
        flowrate = compute_flow_rate(self.fluid,
                                     supply_capacity,
                                     self.supply_temperature,
                                     self.return_temperature)  # [kg/h]

        # Cost -----
        self.global_conversion_efficiency, om_fix_equipment, turnkey_equipment = equipment_details('circulation_pumping', flowrate / fluid_rho)

        # OM VAR Cost -----
        om_var_total = flowrate_to_power(flowrate) * self.fuel_properties['price']  # [kW]*[€/kWh] = [€/h]

        # Create data for TEO ---
        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_equipment,  # [€]
            'om_fix': om_fix_equipment,  # # [€/year]
            'om_var': om_var_total  # [€]
            }

        return info
