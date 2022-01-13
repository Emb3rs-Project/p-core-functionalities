"""
alisboa/jmcunha


##############################
INFO: create solar thermal with all necessary info when performing sources and sinks conversion to the grid.
      The most important attribute of the object is data_teo, which contains all the info necessary for TEO module, such
      as, the equipment turnkey linearized with power, OM fix/variable, emissions, efficiency and others (see below).


##############################
INPUT:
        # country
        # consumer_type - e.g. 'household' or 'non-household'
        # latitude  [º]
        # longitude  [º]
        # yearly_capacity - yearly capacity desired to be supplied [kWh]
        # power_fraction
        # supply_temperature  [ºC]
        # return_temperature  [ºC]


##############################
RETURN: object with all technology info:
        # object_type
        # equipment_sub_type - 'fresnel', 'evacuated_tube' or 'flat_plate'
        # supply_fluid - fluid name
        # fuel_type - fuel name
        # fuel_properties - all fuel properties, e.g. lhv, cost, AFR ..
        # fluid - fluid name
        # supply_temperature  [ºC]
        # return_temperature  [ºC]
        # supply_capacity  [kW]
        # latitude  [º]
        # longitude  [º]
        # C0 - solar thermal coefficient
        # C1
        # C2
        # area_ratio  []
        # yearly_supply_capacity - yearly capacity, before losses, to be supplied [kWh]
        # data_teo - dictionary with equipment data needed by the TEO

            Where in data_teo, the following keys:
                #  equipment - equipment name
                #  fuel_type
                #  max_input_capacity  # [kW]
                #  turnkey_a  # [€/kW]
                #  turnkey_b  # [€]
                #  conversion_efficiency  # []
                #  om_fix  # [€/year.kW]
                #  om_var  # [€/kWh]
                #  emissions  # [kg.CO2/kWh thermal]

"""

import numpy as np
from ....General.Convert_Equipments.Auxiliary.solar_collector_climate_api import solar_collector_climate_api
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....KB_General.equipment_details import equipment_details
from ....KB_General.fuel_properties import fuel_properties
from ....KB_General.fluid_material import fluid_material_rho
from ....KB_General.flowrate_to_power import flowrate_to_power
from ....General.Auxiliary_General.linearize_values import linearize_values


class Add_Solar_Thermal():

    def __init__(self, country, consumer_type, latitude, longitude, stream_available_capacity, power_fraction, supply_temperature, return_temperature):

        # Defined Vars
        self.object_type = 'equipment'
        self.supply_fluid = 'thermal_oil'
        self.fuel_type = 'electricity'
        self.fuel_properties = fuel_properties(country, self.fuel_type, consumer_type)
        hx_delta_T = 5
        hx_efficiency = 0.95
        self.defined_thermal_production = 0.7  # [kW/m2]

        # get equipment characteristics
        self.latitude = latitude
        self.longitude = longitude

        if supply_temperature > 120:
            self.equipment_sub_type = 'fresnel'
            self.C0 = 0.76
            self.C1 = 4.15
            self.C2 = 0.028
            self.area_ratio = 12
        elif supply_temperature > 80:
            self.equipment_sub_type = 'evacuated_tube'
            self.C0 = 0.735
            self.C1 = 1.16
            self.C2 = 0.0053
            self.area_ratio = 1
        else:
            self.equipment_sub_type = 'flat_plate'
            self.C0 = 0.766
            self.C1 = 0.368
            self.C2 = 0.00322
            self.area_ratio = 1

        self.supply_temperature = supply_temperature + hx_delta_T  # HX between Source and Grid
        self.return_temperature = return_temperature + hx_delta_T
        self.stream_available_capacity = stream_available_capacity / hx_efficiency

        # get climate data
        climate = solar_collector_climate_api(self.latitude, self.longitude)  # Get climate data for the location

        # Design Equipment
        # 100% Power
        info_max_power = self.design_equipment(climate, power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(climate, power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['average_supply_capacity'],
                                                info_power_fraction['average_supply_capacity']
                                                )

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_type': self.fuel_type,
            'max_area': info_max_power['area'],  # [m2]
            'max_average_supply_capacity': info_max_power['average_supply_capacity'],  # [kW]
            'hourly_supply_capacity_normalize': info_max_power['hourly_supply_capacity_normalize'],  # [kWh]
            'hourly_supply_capacity': info_max_power['hourly_supply_capacity'],  # [kWh]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': hx_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / info_max_power['average_supply_capacity'],  # [€/year.kW]
            'om_var': info_max_power['om_var'] / info_max_power['average_supply_capacity'],  # [€/kWh]
            'emissions': self.fuel_properties['co2_emissions']  # [kg.CO2/kWh]
        }


    def design_equipment(self, climate, power_fraction):

        # Defined vars
        hx_efficiency = 0.95
        hx_delta_T = 5
        grid_fluid = 'water'
        solar_collector_fluid_rho = fluid_material_rho('thermal_oil',temperature=90)  # [kg/m3]
        grid_supply_temperature = self.supply_temperature - hx_delta_T
        grid_return_temperature = self.return_temperature - hx_delta_T

        # Compute
        vector_solar_collector_flowrate = []
        vector_grid_power = []
        vector_grid_flowrate = []

        # get minimum flowrate allowed - 10% of max power available (day with largest solar radiation)
        matrix = np.array(climate)
        if self.equipment_sub_type == 'flat_plate' or self.equipment_sub_type == "evacuated_tube":
            P_max = max(matrix[:, 2] + matrix[:, 3])  # (Q_beam + Q_dif) for these equipment [W/m2]
        else:
            P_max = max(matrix[:, 2])

        solar_collector_minimum_power = (P_max * 10 ** (-3)) * 0.1  # [kW/m2]
        solar_collector_minimum_flowrate = compute_flow_rate(self.supply_fluid,
                                                             solar_collector_minimum_power,
                                                             self.supply_temperature,
                                                             self.return_temperature)  # [kg/h.m2]

        # compute hourly solar thermal power [kW/m2] and flowrate [kg/h.m2], and grid flowrate [kg/h.m2]
        for index, row in (climate).iterrows():
            T_exterior = row['T_exterior']  # [ºC]
            Q_beam = row['Q_beam_solar_collector']  # [W/m2]
            Q_dif = row['Q_dif_solar_collector']  # [W/m2]

            # get considered incident solar radiation
            if self.equipment_sub_type == 'flat_plate' or self.equipment_sub_type == "evacuated_tube":
                Q_rad = Q_beam + Q_dif  # [W/m2]
            else:
                Q_rad = Q_beam

            # delta T between equipment and ambient air
            delta_T_solar_collector_amb = (self.supply_temperature + self.return_temperature) / 2 - T_exterior

            if Q_rad > 0:
                # compute  efficiency
                eff_solar_collector = self.C0 - self.C1 * (delta_T_solar_collector_amb) / Q_rad - self.C2 * (
                    delta_T_solar_collector_amb) ** 2 / Q_rad

                if eff_solar_collector < 0:
                    eff_solar_collector = 0

                # compute power and flow rate
                solar_collector_power = Q_rad * eff_solar_collector * 10 ** (-3)  # [kW/m2]
                solar_collector_flowrate = compute_flow_rate(self.supply_fluid,
                                                             solar_collector_power,
                                                             self.supply_temperature,
                                                             self.return_temperature)  # [kg/h.m2]

                # check if it meets minimum flow rate requirements
                if solar_collector_flowrate > solar_collector_minimum_flowrate:
                    grid_power = solar_collector_power * hx_efficiency  # [kW/m2]
                    grid_flowrate = compute_flow_rate(grid_fluid,
                                                      grid_power,
                                                      grid_supply_temperature,
                                                      grid_return_temperature)  # [kg/h.m2]
                else:
                    solar_collector_flowrate = 0
                    grid_power = 0
                    grid_flowrate = 0

            else:
                solar_collector_flowrate = 0
                grid_flowrate = 0
                grid_power = 0

            vector_solar_collector_flowrate.append(solar_collector_flowrate)  # [kg/h.m2]
            vector_grid_power.append(grid_power)  # [kW/m2]
            vector_grid_flowrate.append(grid_flowrate)  # [kg/h.m2]

        # compute solar thermal area
        area = (self.stream_available_capacity * power_fraction / self.defined_thermal_production)/ (self.area_ratio)  # [m2]

        # get info
        vector_solar_collector_flowrate = [i * area for i in vector_solar_collector_flowrate]  # [kg/h]
        vector_grid_power = [i * area for i in vector_grid_power]  # [kW]

        # turnkey solar thermal + pumping
        global_conversion_efficiency_equipment, om_fix_equipment, turnkey_equipment = equipment_details(self.equipment_sub_type, area)
        global_conversion_efficiency_equipment_pump, om_fix_equipment_pump, turnkey_equipment_pump = equipment_details(
            'circulation_pumping', max(vector_solar_collector_flowrate) / solar_collector_fluid_rho)  # pump turnkey according to max flowrate possible

        turnkey_total = turnkey_equipment + turnkey_equipment_pump  # [€]

        # OM solar thermal + pumping
        vector_solar_collector_flowrate_power = [flowrate_to_power(i) for i in vector_solar_collector_flowrate]  # [kW]
        om_var_equipment_pump = self.fuel_properties['price'] * max(vector_solar_collector_flowrate_power)  # [€/kWh] * [kWh]

        om_var_total = om_var_equipment_pump  # [€]
        om_fix_total = om_fix_equipment_pump + om_fix_equipment  # [€]

        # get data for TEO
        average_solar_collector_power = sum(vector_grid_power) / (365 * 24)  # [kW]
        vector_grid_power_normalized = [i / average_solar_collector_power for i in
                                        vector_grid_power]  # normalize vector_grid_power with max_solar_collector_power

        info = {
            'area': area,  # [m2]
            'average_supply_capacity': average_solar_collector_power,  # [kW]
            'hourly_supply_capacity_normalize': vector_grid_power_normalized,  # [kWh]
            'hourly_supply_capacity': vector_grid_power,  # [kWh]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€]
            'om_var': om_var_total  # [€]
        }

        return info
