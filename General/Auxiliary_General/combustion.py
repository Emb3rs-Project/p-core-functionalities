"""
@author: jmcunha/alisboa

Info: Compute combustion properties
"""

from ...KB_General.fuel_properties import fuel_properties
from ...KB_General.fluid_material import fluid_material_cp


def combustion_mass_flows (P_equip,eff_equip, fuel_type):
    data = fuel_properties('Portugal',fuel_type,'non_household')  # country and consumer type do not matter
    lhv_fuel = data['lhv_fuel']
    AFR_fuel = data['air_to_fuel_ratio']
    excess_air_fuel = data['excess_air_fuel']

    fuel_consumption = (P_equip/eff_equip)/lhv_fuel  # [kg/h]
    m_air = fuel_consumption * AFR_fuel * excess_air_fuel  # [kg/h]
    m_flue_gas = m_air + fuel_consumption  # [kg/h]

    return fuel_consumption,m_air,m_flue_gas



def T_flue_gas (P_equip,fuel_type, m_fuel,m_flue_gas):
    fluid_type = "flue_gas"

    data = fuel_properties('Portugal', fuel_type, 'non-household')
    lhv_fuel = data['lhv_fuel']

    T_initial = 20 + 274  # [K]

    #Initial guess
    T_it = range(0,3000,5)  # [K]
    T_chamber_max= []


    for i in range(len(T_it)):
        iteration = False
        cp_flue_gas = fluid_material_cp(fluid_type, (T_it[i] + T_initial) / 2)  # [kJ/kg.K]

        while iteration == False:
            T_chamber_new = (lhv_fuel * m_fuel)/(m_flue_gas/3600 * cp_flue_gas) + T_initial # [K]
            cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new+T_initial)/2)  # [kJ/kg.K]

            if (cp_flue_gas_new-cp_flue_gas)<0.00000000000001:
                cp_flue_gas_new = fluid_material_cp(fluid_type, (T_chamber_new + T_initial) / 2)  # [kJ/kg.K]
                cp_flue_gas = cp_flue_gas_new
                T_chamber_max.append(T_chamber_new)
                iteration = True
            else:
                cp_flue_gas = cp_flue_gas_new
                T_chamber_old = T_chamber_new


    T_chamber_max_value = max(T_chamber_max)


    #Initial guess
    fluid_type = 'flue_gas'
    T_it = range(0,1500,50)  # [K]

    count=0

    for num in T_it:
        count+=1

    T_flue_out = []
    for i in range(count):
        iteration = False
        cp_flue_gas = fluid_material_cp(fluid_type, (T_it[i] + T_chamber_max_value) / 2)  # [kJ/kg K]

        i=1
        while iteration == False:
            T_flue_gas_outlet = -P_equip / (m_flue_gas / 3600 * cp_flue_gas) + T_chamber_max_value  # [K]

            i+=1

            cp_flue_gas_new = fluid_material_cp(fluid_type, (T_flue_gas_outlet + T_chamber_max_value) / 2)  # [kJ/kg K]

            if (cp_flue_gas_new-cp_flue_gas)<0.000000001:
                cp_flue_gas_new = fluid_material_cp(fluid_type, (T_flue_gas_outlet + T_chamber_max_value) / 2)  # [kJ/kg K]
                cp_flue_gas = cp_flue_gas_new # kJ/kg K
                T_flue_out.append(T_flue_gas_outlet-274)  # [ºC]
                iteration = True
            else:
                cp_flue_gas = cp_flue_gas_new  # [kJ/kg K]



    T_flue_gas_outlet = min(T_flue_out) # Verify
    inflow_T_outlet = 80

    return T_flue_gas_outlet,inflow_T_outlet



