"""
@author: jmcunha/alisboa

"""

from General.Convert_Equipments.Auxiliary.solar_collector_climate_api import solar_collector_climate_api
import numpy as np
from General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from KB_General.equipment_details import equipment_details
from KB_General.fuel_properties import fuel_properties
from General.Auxiliary_General.flowrate_to_power import flowrate_to_power
from General.Auxiliary_General.linearize_values import linearize_values


class Add_Solar_Thermal():

    def __init__(self,country,consumer_type,latitude,longitude,yearly_capacity,power_fraction,supply_temperature,return_temperature):

        # Defined Vars ----------
        self.object_type = 'equipment'
        self.supply_fluid = 'oil'
        self.fuel_type = 'electricity'
        self.fuel_properties = fuel_properties(country,self.fuel_type,consumer_type)
        hx_delta_T = 5
        hx_efficiency = 0.95

        # INPUT ----
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


        # COMPUTE -----
        self.supply_temperature = supply_temperature + hx_delta_T  # HX between Source and Grid
        self.return_temperature = return_temperature + hx_delta_T
        self.yearly_supply_capacity = yearly_capacity/hx_efficiency

        # Get Climate Data
        self.climate_data() # Get climate data for the location

        # Design Equipment
        # 100% Power
        info_max_power = self.design_equipment(power_fraction=1)

        # Power Fraction
        info_power_fraction = self.design_equipment(power_fraction)

        turnkey_a, turnkey_b = linearize_values(info_max_power['turnkey'],
                                                info_power_fraction['turnkey'],
                                                info_max_power['average_supply_capacity'],
                                                info_power_fraction['average_supply_capacity']
                                                )

        self.data_teo = {
            'equipment': self.equipment_sub_type,
            'fuel_tyoe':self.fuel_type,
            'max_area': info_max_power['area'],  # [m2]
            'max_average_supply_capacity': info_max_power['average_supply_capacity'],  # [kW]
            'hourly_supply_capacity_normalize': info_max_power['hourly_supply_capacity_normalize'],  # [kWh]
            'turnkey_a': turnkey_a,  # [€/kW]
            'turnkey_b': turnkey_b,  # [€]
            'conversion_efficiency': hx_efficiency,  # []
            'om_fix': info_max_power['om_fix'] / info_max_power['average_supply_capacity'],  # [€/year.kW]
            'om_var': info_max_power['om_var'] / info_max_power['average_supply_capacity'],  # [€/kWh]
            'emissions': self.fuel_properties['CO2_emission'] / info_max_power['average_supply_capacity'] # [kg.CO2/kWh]

        }


    def climate_data(self):

        self.climate = solar_collector_climate_api(self.latitude, self.longitude)


    def design_equipment(self,power_fraction):

        # Defined vars --------
        grid_fluid = 'water'
        solar_collector_fluid = 'oil'
        solar_collector_fluid_rho = 800  # [kg/m3]
        hx_efficiency = 0.95
        hx_delta_T = 5
        grid_supply_temperature = self.supply_temperature - hx_delta_T
        grid_return_temperature = self.return_temperature - hx_delta_T

        # Initialize array
        vector_solar_collector_flowrate = []
        vector_grid_power = []
        vector_grid_flowrate = []

        # COMPUTE --------
        # Get minimum flowrate allowed - 10% of max Power (day with largest solar radiation)
        matrix = np.array(self.climate)
        if self.equipment_sub_type == 'flat_plate' or self.equipment_sub_type == "evacuated_tube":
            P_max = max(matrix[:, 2] + matrix[:, 3])  # Q_beam + Q_dif for these equipment [W/m2]
        else:
            P_max = max(matrix[:, 2])

        solar_collector_minimum_power = (P_max * 10 ** (-3)) * 0.1 # [kW/m2]
        solar_collector_minimum_flowrate = compute_flow_rate(self.supply_fluid,
                                                             solar_collector_minimum_power,
                                                             self.supply_temperature,
                                                             self.return_temperature)   # [kg/h.m2]

        # Compute solar thermal power [kW/m2] and flowrate [kg/h.m2], and grid flowrate [kg/h.m2] every hour
        for index, row in (self.climate).iterrows():
            T_amb = row['T_exterior']  # [ºC]
            Q_beam = row['Q_beam_solar_collector']  # [W/m2]
            Q_dif = row['Q_dif_solar_collector']  # [W/m2]

            if self.equipment_sub_type == 'flat_plate' or self.equipment_sub_type == "evacuated_tube":
                Q_rad = Q_beam + Q_dif  # [W/m2]
            else:
                Q_rad = Q_beam

            delta_T_solar_collector_amb = (self.supply_temperature + self.return_temperature) / 2 - T_amb  # delta T between solar thermal and ambient air

            if Q_rad > 0:
                # Compute time step efficiency
                eff_solar_collector = self.C0 - self.C1 * (delta_T_solar_collector_amb) / Q_rad - self.C2 * (
                    delta_T_solar_collector_amb) ** 2 / Q_rad

                if eff_solar_collector < 0:
                    eff_solar_collector = 0

                # Compute power and flowrate
                solar_collector_power = Q_rad * eff_solar_collector * 10**(-3)  # [kW/m2]
                solar_collector_flowrate = compute_flow_rate(self.supply_fluid,
                                                             solar_collector_power,
                                                             self.supply_temperature,
                                                             self.return_temperature)  # [kg/h.m2]

                # Check if meets minimum flowrate requirements
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

            vector_solar_collector_flowrate.append(solar_collector_flowrate)   # [kg/h.m2]
            vector_grid_power.append(grid_power)   # [kW/m2]
            vector_grid_flowrate.append(grid_flowrate)   # [kg/h.m2]

        # Compute Area
        area = (self.yearly_supply_capacity * power_fraction / sum(vector_grid_power)) / (self.area_ratio)  # [m2]
        vector_solar_collector_flowrate = [i*area for i in vector_solar_collector_flowrate]   # [kg/h]
        vector_grid_power = [i*area for i in vector_grid_power]  # [kW]

        # Cost -----
        # Solar Thermal
        global_conversion_efficiency_equipment, om_fix_equipment, turnkey_equipment = equipment_details(self.equipment_sub_type,area)
        global_conversion_efficiency_equipment_pump, om_fix_equipment_pump, turnkey_equipment_pump = equipment_details('circulation_pumping',max(vector_solar_collector_flowrate)/solar_collector_fluid_rho)  # pump turnkey according to max flowrate possible
        #Total
        turnkey_total = turnkey_equipment + turnkey_equipment_pump  # [€]

        # Solar Thermal
        vector_solar_collector_flowrate_to_power = []
        for i in range(len(vector_solar_collector_flowrate)):
            vector_solar_collector_flowrate_to_power.append(flowrate_to_power(i))  # modify vector from flowrate to power - [kg/h] to [kW]  from KB_General
        om_var_equipment_pump = self.fuel_properties['price'] * max(vector_solar_collector_flowrate)  # [€/kWh] * [kWh]
        # Total
        om_var_total = om_var_equipment_pump  # [€]
        om_fix_total = om_fix_equipment_pump + om_fix_equipment  # [€]

        # Create data for TEO ----
        average_solar_collector_power = sum(vector_grid_power)/(365*24)  # [kW]
        vector_grid_power_normalized = [i/average_solar_collector_power for i in vector_grid_power]  # normalize vector_grid_power with max_solar_collector_power

        # Create data for TEO ---
        info = {
            'area': area,  # [m2]
            'average_supply_capacity': average_solar_collector_power,  # [kW]
            'hourly_supply_capacity_normalize': vector_grid_power_normalized,  # [kWh]
            'turnkey': turnkey_total,  # [€]
            'om_fix': om_fix_total,  # [€]
            'om_var': om_var_total  # [€]
            }

        return info



