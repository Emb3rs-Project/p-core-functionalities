from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values


class Add_Thermal_Chiller():
    """
    Create THERMAL CHILLER object with all necessary info when performing sources and sinks conversion to the grid.
    The most important attribute of the object is 'data_teo'' which contains all the info necessary for TEO module.

    Attributes
    ----------
    object_type : str
        DEFAULT="equipment"

    equipment_sub_type : str
        Equipment sub type

    fuel_type : str
        Equipment's fuel

    supply_temperature : float
        Equipment's circuit supply temperature [ºC]

    return_temperature : float
        Equipment's circuit return temperature [ºC]

    supply_capacity : float
        Equipment supply capacity [kW]

    fuel_properties : dict
        Equipment fuel data

    global_conversion_efficiency :
        Equipment efficiency []

    data_teo : dict
        Dictionary with equipment data needed by the TEO

    Methods
    ----------
    design_equipment()
        Get equipment economic data for a specific power fraction

    """

    def __init__(self, kb : KB, fuels_data, supply_capacity, power_fraction):
        """Create THERMAL CHILLER data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        fuels_data: dict
            Fuels price and CO2 emission

        supply_capacity : float
            Equipment supply capacity [kW]

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []
        """

        # Defined Vars
        self.object_type = 'equipment'
        self.equipment_sub_type = 'thermal_chiller'
        self.fuel_type = 'electricity'
        self.supply_temperature = 7  # equipment directly supplies grid/sink/source [ºC]
        self.return_temperature = 12  # [ºC]

        # get equipment characteristics
        self.fuel_properties = fuels_data[self.fuel_type]
        self.supply_capacity = supply_capacity  # equipment directly supplies grid
        equipment_details = EquipmentDetails(kb)
        self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type,
                                                                                           self.supply_capacity)  # get COP

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(kb,power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(kb,power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'] / self.global_conversion_efficiency,
                                                info_power_fraction['supply_capacity'] / self.global_conversion_efficiency
                                                )

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': self.fuel_type,
            'max_input_capacity': info_max_power['supply_capacity'] / self.global_conversion_efficiency,  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency), # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] / self.global_conversion_efficiency  # [kg.CO2/kWh thermal]

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

        supply_capacity = self.supply_capacity * power_fraction  # thermal power supplied [kWh]
        equipment_details = EquipmentDetails(kb)
        global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type, supply_capacity)  # [€]
        electric_power = supply_capacity / self.global_conversion_efficiency  # equipment needed electric power [kW]
        om_var_total = self.fuel_properties['price'] * electric_power  # [€/year]

        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info










