from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values


class Add_CHP():
    """
    Create CHP object with all necessary info when performing sources and sinks conversion to the grid.
    The most important attribute of the object is 'data_teo'' which contains all the info necessary for TEO module.

    Attributes
    ----------
    object_type : str
        DEFAULT="equipment"

    equipment_sub_type : str
        equipment sub type

    fuel_type : str
        equipment's fuel

    supply_temperature : float
        equipment's circuit supply temperature [ºC]

    return_temperature : float
        equipment's circuit return temperature [ºC]

    supply_capacity : float
        equipment supply capacity [kW]

    fuel_properties : dict
        equipment fuel data

    electrical_conversion_efficiency : dict
        equipment electrical conversion efficiency

    thermal_conversion_efficiency : dict
        equipment thermal conversion efficiency

    data_teo : dict
        dictionary with equipment data needed by the TEO

    Methods
    ----------
    design_equipment()
        Get equipment economic data for a specific power fraction

    """


    def __init__(self, kb: KB, fuels_data, fuel_type, supply_capacity, power_fraction, supply_temperature,
                 return_temperature):

        """Create CHP data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        fuels_data: dict:
            Fuels price and CO2 emission

        fuel_type : str
            Equipment's fuel

        supply_capacity : float
            Equipment supply capacity [kW]

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []

        supply_temperature : float
            Equipment's circuit supply temperature [ºC]

        return_temperature : float
            Equipment's circuit return temperature [ºC]

        """

        # Defined Vars
        self.object_type = 'equipment'

        if supply_temperature < 100:
            self.equipment_sub_type = 'chp_gas_engine'
        else:
            self.equipment_sub_type = 'chp_gas_turbine'

        # get equipment characteristics
        self.fuel_type = fuel_type
        self.fuel_properties = fuels_data[fuel_type]
        self.supply_temperature = supply_temperature  # equipment directly supplies grid
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity  # equipment directly supplies grid
        equipment_details = EquipmentDetails(kb)
        all_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type,
                                                                                              supply_capacity)
        self.thermal_conversion_efficiency = all_conversion_efficiency[0]
        self.electrical_conversion_efficiency = all_conversion_efficiency[1]

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(kb, power_fraction=1)
        # Power Fraction
        info_power_fraction = self.design_equipment(kb, power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'] / self.thermal_conversion_efficiency,
                                                info_power_fraction['supply_capacity'] / self.thermal_conversion_efficiency
                                                )

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': self.fuel_type,
            'max_input_capacity': info_max_power['supply_capacity'] / self.thermal_conversion_efficiency,  # [kW]
            'electrical_generation': info_max_power['electrical_generation'],  # [kWe]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.thermal_conversion_efficiency,  # []
            'electrical_conversion_efficiency': self.electrical_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (
                    info_max_power['supply_capacity'] / self.thermal_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (
                    info_max_power['supply_capacity'] / self.thermal_conversion_efficiency),  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] / self.thermal_conversion_efficiency
            # [kg.CO2/kWh thermal]
        }

    def design_equipment(self, kb, power_fraction):
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

        supply_capacity = self.supply_capacity * (power_fraction)  # thermal power needed [kW]
        electrical_generation = supply_capacity / (self.thermal_conversion_efficiency) * (
            self.electrical_conversion_efficiency)  # [kW]

        equipment_details = EquipmentDetails(kb)
        all_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(self.equipment_sub_type,
                                                                                              supply_capacity)
        fuel_power_equipment = supply_capacity / self.thermal_conversion_efficiency
        om_var_total = self.fuel_properties['price'] * fuel_power_equipment

        info = {
            'electrical_generation': electrical_generation,
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info
