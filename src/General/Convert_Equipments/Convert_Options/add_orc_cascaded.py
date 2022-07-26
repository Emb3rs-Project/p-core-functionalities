from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values

class Add_ORC_Cascaded():
    """
    Create ORC CASCADED object with all necessary info when performing sources and sinks conversion to the grid.
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

    supply_capacity : float
        Equipment thermal supply capacity [kW]

    overall_thermal_capacity : float
        Convertible thermal supply capacity [kW]

    electrical_generation
        Equipment electrical capacity [kWe]

    data_teo : dict
        Dictionary with equipment data needed by the TEO

    """

    def __init__(self, kb : KB, orc_cond_temperature_supply, equipment_sub_type, overall_thermal_capacity, electrical_generation, power_fraction):
        """Create ORC CASCADED

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        orc_cond_temperature_supply : float
            ORC condenser temperature [ºC]

        equipment_sub_type : str
            DEFAULT="orc"

        overall_thermal_capacity : float
            Convertible thermal supply capacity [kW]

        electrical_generation : float
            Electrical supply capacity [kWe]

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []

        """

        # Defined Vars
        self.object_type = 'equipment'
        self.fuel_type = 'electricity'

        # get equipment characteristics
        self.equipment_sub_type = equipment_sub_type  # orc
        self.supply_temperature = orc_cond_temperature_supply  # max water temperature
        self.overall_thermal_capacity = overall_thermal_capacity
        self.electrical_generation = electrical_generation  # electrical supply capacity [kW]

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(kb,power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(kb,power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'] / info_max_power['conversion_efficiency'],
                                                info_power_fraction['supply_capacity'] / info_power_fraction['conversion_efficiency']
                                                )

        self.supply_capacity = info_max_power['supply_capacity']

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': self.fuel_type,
            'max_eletrical_generation': info_max_power['electrical_generation'],  # [kW]
            'max_input_capacity': info_max_power['supply_capacity'] / info_max_power['conversion_efficiency'],  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': info_max_power['conversion_efficiency'],  # []
            'electrical_conversion_efficiency': info_max_power['electrical_generation'] / (info_max_power['supply_capacity'] / info_max_power['conversion_efficiency']),
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] / info_max_power['conversion_efficiency']),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / info_max_power['conversion_efficiency']),  # [€/kWh]
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

        # Defined Vars
        hx_efficiency = 0.95

        # get info
        overall_thermal_capacity = self.overall_thermal_capacity * power_fraction
        electrical_generation = self.electrical_generation * power_fraction  # electrical supply capacity [kW]
        supply_capacity = (overall_thermal_capacity - electrical_generation) * hx_efficiency  # thermal supply capacity [kW]

        equipment_details = EquipmentDetails(kb)
        global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type, electrical_generation)
        om_var_total = 0

        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total,  # [€]
            'conversion_efficiency': supply_capacity / overall_thermal_capacity,  #
            'electrical_generation': electrical_generation
        }

        return info
