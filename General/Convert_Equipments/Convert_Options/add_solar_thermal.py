import numpy as np
from ....General.Convert_Equipments.Auxiliary.solar_collector_climate_api import solar_collector_climate_api
from ....General.Auxiliary_General.compute_flow_rate import compute_flow_rate
from ....General.Auxiliary_General.linearize_values import linearize_values
from ....KB_General.equipment_details import EquipmentDetails
from ....KB_General.fuel_properties import FuelProperties
from ....KB_General.medium import Medium
from ....KB_General.flowrate_to_power import flowrate_to_power
from ....utilities.kb import KB


class Add_Solar_Thermal():
    """
    Create SOLAR THERMAL object with all necessary info when performing sources and sinks conversion to the grid.
    The most important attribute of the object is 'data_teo'' which contains all the info necessary for TEO module.

    Attributes
    ----------
    object_type : str
        DEFAULT="equipment"

    supply_fluid : str
        Solar thermal circuit fluid; DEFAULT="thermal_oil"

    fuel_type : str
        DEFAULT="electricity"

    fuel_properties : dict
        Equipment fuel data

    equipment_sub_type : str
        'fresnel', 'evacuated_tube' or 'flat_plate'

    supply_temperature : float
        Equipment's circuit supply temperature [ºC]

    return_temperature : float
        Equipment's circuit return temperature [ºC]

    stream_available_capacity : float
        Desired nominal supply capacity [kW]

    C0 : float
        C0 parameter solar thermal

    C1 : float
        C1 parameter solar thermal

    C2 : float
        C2 parameter solar thermal

    area_ratio : float
        Solar thermal panels area to ground area ratio

    data_teo : dict
        Dictionary with equipment data needed by the TEO

    """

    def __init__(self, kb : KB,fuels_data,  latitude, longitude, stream_available_capacity, power_fraction, supply_temperature, return_temperature,hx_delta_T,hx_efficiency):

        """Create SOLAR THERMAL data

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        fuels_data: dict
            Fuels price and CO2 emission

        latitude : float
            Location latitude [ºC]

        longitude : float
            Longitude latitude [ºC]

        stream_available_capacity : float
            Desired nominal supply capacity [kW]

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []

        supply_temperature : float
            Equipment's circuit supply temperature [ºC]

        return_temperature : float
            Equipment's circuit return temperature [ºC]

        hx_delta_T : float
            Heat exchanger temperature difference [ºC]

        hx_efficiency : float
            Heat exchanger efficiency []

        """

        # Defined Vars
        self.object_type = 'equipment'
        self.supply_fluid = 'thermal_oil'
        self.fuel_type = 'electricity'

        fuel_properties = FuelProperties(kb)
        self.fuel_properties = fuels_data[self.fuel_type]

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
        info_max_power = self.design_equipment(kb,climate, hx_delta_T, hx_efficiency, power_fraction=1)
        # power fraction
        info_power_fraction = self.design_equipment(kb,climate, hx_delta_T, hx_efficiency, power_fraction)

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


    def design_equipment(self,kb, climate, hx_delta_T, hx_efficiency, power_fraction):

        """Get equipment techno-economic data for a specific power fraction

        Parameters
        ----------
        kb : dict
            Knowledge Base data

        hx_delta_T : float
            Heat exchangers temperature difference [ºC]

        hx_efficiency : float
            Heat exchangers efficiency []

        power_fraction : float
            Design equipment for max and fraction power; value between 0 and 1 []

        Returns
        -------
        info : dict
            Designed equipment techno-economic data

        """

        # Defined vars
        grid_fluid = 'water'
        medium = Medium(kb)
        solar_collector_fluid_rho = medium.rho('thermal_oil',temperature=90)  # [kg/m3]
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

        solar_collector_minimum_flowrate = compute_flow_rate(kb, self.supply_fluid,
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
                solar_collector_flowrate = compute_flow_rate(kb,self.supply_fluid,
                                                             solar_collector_power,
                                                             self.supply_temperature,
                                                             self.return_temperature)  # [kg/h.m2]

                # check if it meets minimum flow rate requirements
                if solar_collector_flowrate > solar_collector_minimum_flowrate:
                    grid_power = solar_collector_power * hx_efficiency  # [kW/m2]
                    grid_flowrate = compute_flow_rate(kb,grid_fluid,
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
        max_power = max(vector_grid_power)
        area = (self.stream_available_capacity * power_fraction / max_power)/ (self.area_ratio)  # [m2]

        # get info
        vector_solar_collector_flowrate = [i * area for i in vector_solar_collector_flowrate]  # [kg/h]
        vector_grid_power = [i * area for i in vector_grid_power]  # [kW]

        # turnkey solar thermal + pumping
        equipment_details = EquipmentDetails(kb)
        global_conversion_efficiency_equipment, om_fix_equipment, turnkey_equipment = equipment_details.get_values(self.equipment_sub_type, area)
        global_conversion_efficiency_equipment_pump, om_fix_equipment_pump, turnkey_equipment_pump = equipment_details.get_values(
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
