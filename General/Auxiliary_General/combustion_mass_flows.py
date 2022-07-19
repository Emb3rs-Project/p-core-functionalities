from ...KB_General.fuel_properties import FuelProperties
from ...utilities.kb import KB


def combustion_mass_flows(kb : KB, power_equipment, eff_equip, fuel_type):
    """Characterize equipment combustion fuel, air and flue gas flowrate

    Parameters
    ----------
    kb : dict
        Knowledge Base data

    power_equipment :

    eff_equip : float
        Equipment efficiency []

    fuel_type : str
        Fuel name

    Returns
    -------
    fuel_consumption : float
        Fuel mass flowrate [kg/h]

    m_air : float
        Air mass flowrate [kg/h]

    m_flue_gas : float
        Flue gas mass flowrate [kg/h]

    """

    # get fuel data
    fuel_properties = FuelProperties(kb)
    fuel_data = fuel_properties.get_values('Portugal', fuel_type, 'non_household')  # country and consumer type do not matter
    lhv_fuel = fuel_data['lhv_fuel']
    AFR_fuel = fuel_data['air_to_fuel_ratio']
    excess_air_fuel = fuel_data['excess_air_fuel']

    # compute mass flows
    fuel_consumption = (power_equipment / eff_equip) / lhv_fuel  # [kg/h]
    m_air = fuel_consumption * AFR_fuel * excess_air_fuel  # [kg/h]
    m_flue_gas = m_air + fuel_consumption  # [kg/h]

    return fuel_consumption, m_air, m_flue_gas


