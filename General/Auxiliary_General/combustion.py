"""
alisboa/jmcunha


------------------------------ combustion_mass_flows
##############################
INFO: characterize equipment combustion fuel, air and flue_gas flowrate.

##############################
INPUT:
        # power_equipment  [kW]
        # eff_equip  []
        # fuel_type - e.g. natural_gas, fuel_oil,biomass

##############################
RETURN:
        # fuel_consumption  [kg/h]
        # m_air  [kg/h]
        # m_flue_gas  [kg/h]


------------------------------ compute_flue_gas_temperature
##############################
INFO: very simplified estimate of the equipment flue gas temperature

##############################
INPUT:
        # power_equipment  [kW]
        # fuel_type - e.g. natural_gas, fuel_oil,biomass
        # m_fuel  [kg/h]
        # m_flue_gas  [kg/h]

##############################
RETURN:
        # T_flue_gas_outlet  [ºC]
        # inflow_T_outlet  [ºC]



"""

from ...KB_General.fuel_properties import fuel_properties
from ...KB_General.fluid_material import fluid_material_cp


def combustion_mass_flows(power_equipment, eff_equip, fuel_type):

    # get fuel data
    fuel_data = fuel_properties('Portugal', fuel_type, 'non_household')  # country and consumer type do not matter
    lhv_fuel = fuel_data['lhv_fuel']
    AFR_fuel = fuel_data['air_to_fuel_ratio']
    excess_air_fuel = fuel_data['excess_air_fuel']

    # compute mass flows
    fuel_consumption = (power_equipment / eff_equip) / lhv_fuel  # [kg/h]
    m_air = fuel_consumption * AFR_fuel * excess_air_fuel  # [kg/h]
    m_flue_gas = m_air + fuel_consumption  # [kg/h]

    return fuel_consumption, m_air, m_flue_gas


def compute_flue_gas_temperature(power_equipment, fuel_type, m_fuel, m_flue_gas):

    # init vars
    fluid_type = "flue_gas"
    initial_temperature = 20 + 274  # considered air temperature  [K]

    # get fuel data
    fuel_data = fuel_properties('Portugal', fuel_type, 'non-household')
    lhv_fuel = fuel_data['lhv_fuel']

    # iterate until simplified estimate of chamber temperature
    T_it = range(0, 3000, 5)  # give random initial values to test the convergence [K]
    T_chamber_max = []

    for i in range(len(T_it)):
        iteration = False
        cp_flue_gas = fluid_material_cp(fluid_type, (T_it[i] + initial_temperature) / 2)  # [kJ/kg.K]

        while iteration == False:
            T_chamber_new = (lhv_fuel * m_fuel) / (m_flue_gas / 3600 * cp_flue_gas) + initial_temperature  # [K]
            cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new + initial_temperature) / 2)  # [kJ/kg.K]

            if (cp_flue_gas_new - cp_flue_gas) < 10**(-5):
                cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new + initial_temperature) / 2)  # [kJ/kg.K]
                cp_flue_gas = cp_flue_gas_new
                T_chamber_max.append(T_chamber_new)
                iteration = True
            else:
                cp_flue_gas = cp_flue_gas_new

    T_chamber_max_value = max(T_chamber_max)

    # iterate until simplified estimate of flue gas temperature
    T_it = range(0, 1500, 50)  # give random initial values to test the convergence [K]
    vector_T_flue_gas = []

    for i in range(len(T_it)):
        iteration = False
        cp_flue_gas = fluid_material_cp(fluid_type, (T_it[i] + T_chamber_max_value) / 2)  # [kJ/kg K]

        while iteration == False:

            T_flue_gas_outlet = -power_equipment / (m_flue_gas / 3600 * cp_flue_gas) + T_chamber_max_value  # [K]
            cp_flue_gas_new = fluid_material_cp(fluid_type, (T_flue_gas_outlet + T_chamber_max_value) / 2)  # [kJ/kg K]

            if (cp_flue_gas_new - cp_flue_gas) < 10**(-5):
                cp_flue_gas_new = fluid_material_cp(fluid_type,(T_flue_gas_outlet + T_chamber_max_value) / 2)  # [kJ/kg K]
                cp_flue_gas = cp_flue_gas_new  # [kJ/kg K]
                vector_T_flue_gas.append(T_flue_gas_outlet - 274)  # [ºC]
                iteration = True
            else:
                cp_flue_gas = cp_flue_gas_new  # [kJ/kg K]

    # get output
    T_flue_gas_outlet = min(vector_T_flue_gas)  # [ºC]
    inflow_T_outlet = 80  # [ºC]

    return T_flue_gas_outlet, inflow_T_outlet


def burner_chamber_temperature(fuel_type, m_fuel, m_flue_gas):

    # init vars
    fluid_type = "flue_gas"
    initial_temperature = 20 + 274  # considered air temperature  [K]

    # get fuel data
    fuel_data = fuel_properties('Portugal', fuel_type, 'non-household')
    lhv_fuel = fuel_data['lhv_fuel']

    # iterate until simplified estimate of chamber temperature
    T_it = range(0, 3000, 5)  # give random initial values to test the convergence [K]
    T_chamber_max = []

    for i in range(len(T_it)):
        iteration = False
        cp_flue_gas = fluid_material_cp(fluid_type, (T_it[i] + initial_temperature) / 2)  # [kJ/kg.K]

        while iteration == False:
            T_chamber_new = (lhv_fuel * m_fuel) / (m_flue_gas / 3600 * cp_flue_gas) + initial_temperature  # [K]
            cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new + initial_temperature) / 2)  # [kJ/kg.K]

            if (cp_flue_gas_new - cp_flue_gas) < 10**(-5):
                cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new + initial_temperature) / 2)  # [kJ/kg.K]
                cp_flue_gas = cp_flue_gas_new
                T_chamber_max.append(T_chamber_new)
                iteration = True
            else:
                cp_flue_gas = cp_flue_gas_new

    T_chamber_max_value = max(T_chamber_max)


    return T_chamber_max_value