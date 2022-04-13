"""
alisboa/jmcunha


##############################
INFO: create heat exchanger object with all necessary info when performing sources and sinks conversion to the grid.
      The most important attribute of the object is data_teo, which contains all the info necessary for TEO module, such
      as, the equipment turnkey linearized with power, OM fix/variable, emissions, efficiency and others (see below).


##############################
INPUT:
        # hot_stream_T_hot  [ºC]
        # hot_stream_T_cold  [ºC]
        # hot_stream_fluid - fluid name
        # cold_stream_T_hot  [ºC]
        # cold_stream_T_cold  [ºC]
        # cold_stream_fluid - fluid name
        # power - nominal design power, not considering efficiency  [kW]
        # power_fraction - design equipment for max and fraction power; value between 0 and 1


##############################
RETURN: object with all technology info:
        # object_type
        # equipment_sub_type
        # power - nominal design power, not considering efficiency  [kW]
        # available_power - effective hx power; considers efficiency  [kW]
        # hot_stream_T_hot  [ºC]
        # hot_stream_T_cold  [ºC]
        # cold_stream_T_hot  [ºC]
        # cold_stream_T_cold  [ºC]
        # u_value  [W/K.m2]
        # global_conversion_efficiency  []
        # data_teo - dictionary with equipment data needed by the TEO

            Where in data_teo, the following keys:
                #  equipment - equipment name
                #  fuel_type
                #  max_input_capacity - max power the equipment can convert [kW]
                #  turnkey_a  [€/kW]
                #  turnkey_b  [€]
                #  conversion_efficiency   []
                #  om_fix  [€/year.kW]
                #  om_var  [€/kWh]
                #  emissions   [kg.CO2/kWh thermal]

"""


from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....KB_General.hx_data import HxData
from ....General.Auxiliary_General.compute_delta_T_lmtd import compute_delta_T_lmtd_counter

class Add_HX():

    def __init__(self, kb : KB, hot_stream_T_hot, hot_stream_T_cold, hot_stream_fluid, cold_stream_T_hot, cold_stream_T_cold,
                 cold_stream_fluid, power, power_fraction):

        # Defined Vars
        self.object_type = 'equipment'
        hx_efficiency = 0.95  # defined hx efficiency

        # get equipment characteristics
        self.power = power
        self.available_power = power * hx_efficiency
        self.hot_stream_T_hot = hot_stream_T_hot
        self.hot_stream_T_cold = hot_stream_T_cold
        self.cold_stream_T_hot = cold_stream_T_hot
        self.cold_stream_T_cold = cold_stream_T_cold

        hx_data = HxData(kb)
        self.equipment_sub_type, self.u_value = hx_data.get_values(hot_stream_fluid, cold_stream_fluid)

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(kb,power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(kb,power_fraction)
        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'],
                                                info_power_fraction['supply_capacity']
                                                )


        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': 'none',
            'max_input_capacity': info_max_power['supply_capacity'],  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity']),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity']),  # [€/kWh]
            'emissions': 0  # [kg.CO2/kWh]
        }


    def design_equipment(self,kb, power_fraction):

        hx_power = self.power * power_fraction

        if self.equipment_sub_type == 'hx_economizer':
            hx_char = abs(hx_power)  # Gas cooler - characteristic value is Power  [kW]
        else:
            self.delta_T_lmtd = compute_delta_T_lmtd_counter(self.hot_stream_T_hot, self.hot_stream_T_cold, self.cold_stream_T_hot, self.cold_stream_T_cold)
            hx_char = abs(hx_power) / (self.u_value / 1000 * self.delta_T_lmtd)  # Plate/Shell&tubes - characteristic value is Area  [m2]


        equipment_details = EquipmentDetails(kb)
        self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type, hx_char)
        om_var_total = 0  # om variable considered negligible

        info = {
            'supply_capacity': hx_power,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info







