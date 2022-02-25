"""
alisboa/jmcunha


##############################
INFO: create boiler object with all necessary info when performing sources and sinks conversion to the grid.
      The most important attribute of the object is data_teo, which contains all the info necessary for TEO module, such
      as, the equipment turnkey linearized with power, OM fix/variable, emissions, efficiency and others (see below).


##############################
INPUT:
        # fuel_type
        # country
        # consumer_type - e.g. 'household' or 'non-household'
        # supply_capacity  [kW]
        # power_fraction - design equipment for max and fraction power; value between 0 and 1
        # supply_temperature  [ºC]
        # return_temperature  [ºC]


##############################
RETURN: object with all technology info:
        # object_type
        # equipment_sub_type
        # fuel_type
        # country
        # global_conversion_efficiency  []
        # fuel_properties
        # supply_temperature  [ºC]
        # return_temperature  [ºC]
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
from ....KB_General.fuel_properties import FuelProperties
from ....General.Auxiliary_General.linearize_values import linearize_values


class Add_Boiler():

    def __init__(self, kb: KB, fuel_type, country, consumer_type, supply_capacity, power_fraction, supply_temperature,
                 return_temperature):

        # Defined Vars
        self.object_type = 'equipment'

        if supply_temperature > 100:
            self.equipment_sub_type = 'steam_boiler'
        else:
            self.equipment_sub_type = 'hot_water_boiler'

        # get equipment characteristics
        self.fuel_type = fuel_type
        self.supply_temperature = supply_temperature  # equipment directly supplies grid
        self.return_temperature = return_temperature
        self.supply_capacity = supply_capacity
        fuel_properties = FuelProperties(kb)
        self.fuel_properties = fuel_properties.get_values(country, self.fuel_type, consumer_type)


        if fuel_type == 'electricity':
            self.global_conversion_efficiency = 0.99
        else:
            equipment_details = EquipmentDetails(kb)
            self.global_conversion_efficiency, om_fix_total, turnkey_total = equipment_details.get_values(
                self.equipment_sub_type, self.supply_capacity)

        # Design Equipment
        # 100% power
        info_max_power = self.design_equipment(kb,power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(kb,power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['supply_capacity'] / self.global_conversion_efficiency,
                                                info_power_fraction[
                                                    'supply_capacity'] / self.global_conversion_efficiency
                                                )

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': self.fuel_type,
            'max_input_capacity': info_max_power['supply_capacity'] / self.global_conversion_efficiency,  # [kW]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': self.global_conversion_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / (
                        info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/year.kW]
            'om_var': info_max_power['om_var'] / (
                        info_max_power['supply_capacity'] / self.global_conversion_efficiency),  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions'] / self.global_conversion_efficiency
            # [kg.CO2/kWh thermal]
        }


    def design_equipment(self,kb, power_fraction):

        supply_capacity = self.supply_capacity * power_fraction  # [kW]

        equipment_details = EquipmentDetails(kb)
        global_conversion_efficiency_equipment, om_fix_total, turnkey_total = equipment_details.get_values(
            self.equipment_sub_type, supply_capacity)

        fuel_power_equipment = supply_capacity / self.global_conversion_efficiency  # fuel power to get equipment running
        om_var_total = self.fuel_properties['price'] * fuel_power_equipment

        info = {
            'supply_capacity': supply_capacity,  # [kW]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€/year]
            'om_var': om_var_total  # [€]
        }

        return info
