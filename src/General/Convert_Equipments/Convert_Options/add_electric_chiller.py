from ....utilities.kb import KB
from ....KB_General.equipment_details import EquipmentDetails
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....General.Auxiliary_General.compute_cop_eer import compute_cop_eer


class Add_Electric_Chiller():
    """
    Create ELECTRIC CHILLER object with all necessary info when performing sources and sinks conversion to the grid.
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

    global_conversion_efficiency :
        equipment efficiency; COP []

    data_teo : dict
        dictionary with equipment data needed by the TEO

    Methods
    ----------
    design_equipment()
        Get equipment economic data for a specific power fraction

    """

    def __init__(self, kb: KB, fuels_data, supply_capacity, power_fraction, supply_temperature, return_temperature):
        """Create ELECTRIC CHILLER data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        fuels_data: dict:
            Fuels price and CO2 emission

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
        self.equipment_sub_type = 'compression_chiller'
        self.fuel_type = 'electricity'


        # get equipment characteristics
        self.fuel_properties = fuels_data[self.fuel_type]
        self.supply_temperature = supply_temperature  # equipment directly supplies grid/sink/source [ºC]
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity  # heat supply capacity [kW]
        self.cop = compute_cop_eer(self.equipment_sub_type,evaporator_temperature=self.supply_temperature)  # COP
        self.evap_capacity = self.supply_capacity * (1 - 1 / self.cop)
        self.global_conversion_efficiency = self.supply_capacity/self.evap_capacity # actually this is heat output/heat_input so that every equipment is the same

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
            'fuel_type': self.fuel_type,
            'max_input_capacity': info_max_power['supply_capacity'] / self.global_conversion_efficiency,  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/kWh]
            'emissions': (self.fuel_properties['co2_emissions']/self.cop) / self.global_conversion_efficiency  # [kg.CO2/kWh electric]
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

        supply_capacity = self.supply_capacity * power_fraction  # thermal power supplied [kW]
        electric_power_equipment = supply_capacity / self.cop  # equipment needed electric power [kW]
        equipment_details = EquipmentDetails(kb)
        global_conversion_efficiency_equipment, om_fix_total, turnkey_equipment = equipment_details.get_values(self.equipment_sub_type, supply_capacity)
        om_var_total = self.fuel_properties['price'] * electric_power_equipment  # [€]

        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_equipment,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info











