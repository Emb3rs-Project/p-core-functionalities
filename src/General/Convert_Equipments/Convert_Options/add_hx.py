from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....KB_General.hx_data import HxData
from ....General.Auxiliary_General.compute_delta_T_lmtd import compute_delta_T_lmtd_counter

class Add_HX():
    """
    Create HEAT EXCHANGER object with all necessary info when performing sources and sinks conversion to the grid.
    The most important attribute of the object is 'data_teo'' which contains all the info necessary for TEO module.

    Attributes
    ----------
    object_type : str
        DEFAULT="equipment"

    equipment_sub_type : str
        Equipment sub type

    power : float
        Nominal design power, not considering efficiency  [kW]

    available_power
        Effective hx power; considers efficiency  [kW]

    hot_stream_T_hot : float
        Hot stream's hot/higher temperature [ºC]

    hot_stream_T_cold : float
        Hot stream's cold/lower temperature [ºC]

     hot_stream_fluid : str
        Hot stream fluid

    cold_stream_T_hot : float
        Hot stream's hot/higher temperature [ºC]

    cold_stream_T_cold : float
        Cold stream's cold/lower temperature [ºC]

    cold_stream_fluid : str
        Cold stream fluid

    delta_T_lmtd : float
        Logarithmic mean temperature difference

    u_value : float
        Equipment U value [W/m2.K]

    global_conversion_efficiency : float
        Equipment efficiency []

    data_teo : dict
        Dictionary with equipment data needed by the TEO

    Methods
    ----------
    design_equipment()
        Get equipment economic data for a specific power fraction
    """

    def __init__(self, kb : KB, hot_stream_T_hot, hot_stream_T_cold, hot_stream_fluid, cold_stream_T_hot, cold_stream_T_cold,
                 cold_stream_fluid, power, power_fraction):

        """Create HEAT EXCHANGER data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        hot_stream_T_hot : float
            Hot stream's hot/higher temperature

        hot_stream_T_cold : float
            Hot stream's cold/lower temperature

        hot_stream_fluid : str
            Hot stream fluid

        cold_stream_T_hot : float
            Hot stream's hot/higher temperature

        cold_stream_T_cold : float
            Cold stream's cold/lower temperature

        cold_stream_fluid : str
            Cold stream fluid

        power : float
            Nominal design power, not considering efficiency  [kW]

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []
        """

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
        """Get equipment economic data for a specific power fraction

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []

        Returns
        -------
        info : dict
            Designed equipment economic data

        """
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







