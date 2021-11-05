"""
@author: jmcunha/alisboa

"""

from ....KB_General.equipment_details import equipment_details
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....KB_General.hx_type_and_u import hx_type_and_u


import numpy as np

class Add_HX():

    def __init__(self,hot_stream_T_hot, hot_stream_T_cold, hot_stream_fluid, cold_stream_T_hot, cold_stream_T_cold,cold_stream_fluid, power, power_fraction):

        # Defined Vars ----
        self.object_type = 'equipment'
        hx_efficiency = 0.95

        # INPUT ----
        # Equipment
        self.power = power
        self.available_power = power * hx_efficiency

        self.hot_stream_T_hot = hot_stream_T_hot
        self.hot_stream_T_cold = hot_stream_T_cold
        self.cold_stream_T_hot = cold_stream_T_hot
        self.cold_stream_T_cold = cold_stream_T_cold


        # COMPUTE
        # Design Equipment
        self.equipment_sub_type, self.u_value = hx_type_and_u(hot_stream_fluid,cold_stream_fluid)
        self.compute_delta_T_lmtd_counter()

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
            'equipment':self.equipment_sub_type,
            'fuel_type': 'none',
            'max_input_capacity':info_max_power['supply_capacity'],  # [kW]
            'turnkey_a':turnkey_a,  # [€/kW]
            'turnkey_b':turnkey_b,  # [€]
            'conversion_efficiency':self.global_conversion_efficiency,  # []
            'om_fix':info_max_power['om_fix'] / (info_max_power['supply_capacity'] ),
            # [€/year.kW]
            'om_var':info_max_power['om_var'] / (info_max_power['supply_capacity'] ),
            # [€/kWh]
            'emissions':0  # [kg.CO2/kWh]
            }




    def design_equipment(self, power_fraction):

        # HX info
        hx_power = self.power * power_fraction

        # HX turnkey/om_fix cost
        if self.equipment_sub_type == 'hx_economizer':
            hx_char = abs(hx_power)  # Gas cooler - Power
        else:
            hx_char = abs(hx_power) / (self.u_value / 1000 * self.delta_T_lmtd)  # Plate/Shell&tubes - Area

        self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details(self.equipment_sub_type, hx_char)
        om_var_total = 0

        # Create data for TEO ---
        info = {
            'supply_capacity': hx_power,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info


    def compute_delta_T_lmtd_counter(self):

        delta_T_in = abs(self.hot_stream_T_hot - self.cold_stream_T_hot)
        delta_T_out = abs(self.hot_stream_T_cold - self.cold_stream_T_cold)

        if delta_T_in == delta_T_out:
            delta_T_lmtd = delta_T_in
        else:
            delta_T_lmtd = (delta_T_in - delta_T_out) / np.log(delta_T_in / delta_T_out)

        self.delta_T_lmtd = delta_T_lmtd






