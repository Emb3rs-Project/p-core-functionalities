from ..KB_General.fuel_properties import FuelProperties
from ..General.Auxiliary_General.get_country import get_country
from ..utilities.kb import KB

def fuel_data_fill_values(location, fuels_data, kb : KB):

    fuels = FuelProperties(kb)
    country = get_country(location[0], location[1])

    for fuel in fuels_data.keys():
        fuel_data = fuels.get_values(country, fuel)

        if fuels_data[fuel]["price"] == None:
            fuels_data[fuel]["price"] = fuel_data["price"]

        if fuels_data[fuel]["co2_emissions"] == None:
            fuels_data[fuel]["co2_emissions"] = fuel_data["co2_emissions"]

    return fuels_data