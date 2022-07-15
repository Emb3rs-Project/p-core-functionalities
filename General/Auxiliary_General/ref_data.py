from module.General.Auxiliary_General.get_country import get_country
from module.KB_General.fuel_properties import FuelProperties


def ref_data(ref_system_fuel_type,ref_system_fuel_price,location,consumer_type,kb):

    if ref_system_fuel_type != "none":
        latitude, longitude = location
        fuel_properties = FuelProperties(kb)
        country = get_country(latitude, longitude)

        fuel_data = fuel_properties.get_values(country, ref_system_fuel_type, consumer_type)

        if ref_system_fuel_price == "none":
            fuel_price = ref_system_fuel_price
        else:
            fuel_price = fuel_data["price"]

        fuel_co2_emissions = fuel_data["co2_emissions"]
    else:
        fuel_co2_emissions = 0
        fuel_price = 0

    return fuel_co2_emissions, fuel_price