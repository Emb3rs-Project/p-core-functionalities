from ....utilities.kb import KB
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....KB_General.equipment_details import EquipmentDetails
from ....KB_General.flowrate_to_power import flowrate_to_power
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....KB_General.medium import Medium


class Add_Pump():
    """
    Create PUMPING object with all necessary info when performing sources and sinks conversion to the grid.
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

    fluid : str
        Fluid pumped

    data_teo : dict
        Dictionary with equipment data needed by the TEO

    Methods
    ----------
    design_equipment()
        Get equipment economic data for a specific power fraction

    """

    def __init__(self, kb: KB, fuels_data,  fluid, supply_capacity, power_fraction, supply_temperature,
                 return_temperature):
        """Create PUMPING data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        fuels_data: dict
            Fuels price and CO2 emission

        fluid : str
            Fluid pumped

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
        self.equipment_sub_type = 'circulation_pumping'
        self.fuel_type = 'electricity'

        # get equipment characteristics
        self.fuel_properties = fuels_data[self.fuel_type]
        self.fluid = fluid
        self.supply_temperature = supply_temperature
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity

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
            'max_input_capacity': info_max_power['supply_capacity'],  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (info_max_power['supply_capacity']),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (info_max_power['supply_capacity']),  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] * (
                        info_max_power['om_var'] / self.fuel_properties['price'])
                         / (info_max_power['supply_capacity'])  # [kg.CO2/kWh]
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

        medium = Medium(kb)
        fluid_rho = medium.rho(self.fluid, (self.supply_temperature + self.return_temperature) / 2)  # [kg/m3]
        supply_capacity = self.supply_capacity * power_fraction  # thermal power supplied [kWh]

        flowrate = compute_flow_rate(kb,
                                     self.fluid,
                                     supply_capacity,
                                     self.supply_temperature,
                                     self.return_temperature)  # [kg/h]

        equipment_details = EquipmentDetails(kb)
        self.global_conversion_efficiency, om_fix_equipment, turnkey_equipment = equipment_details.get_values(
            'circulation_pumping', flowrate / fluid_rho)
        om_var_total = flowrate_to_power(flowrate / fluid_rho) * self.fuel_properties['price']  # [kW]*[€/kWh] = [€/h]

        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_equipment,  # [€]
            'om_fix': om_fix_equipment,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info
