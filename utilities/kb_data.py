import json
import os


def load_db():
    script_dir = os.path.dirname(__file__)

    building_properties = json.load(
        open(os.path.join(script_dir, "Json_files", "building_properties.json"))
    )

    equipment_details = json.load(
        open(os.path.join(script_dir, "Json_files", "equipment_details.json"))
    )
    medium_list = json.load(
        open(os.path.join(script_dir, "Json_files", "medium_list.json")))

    fuel_properties = json.load(
        open(os.path.join(script_dir, "Json_files", "fuel_properties.json")))


    eu_country_acronym = json.load(
        open(os.path.join(script_dir, "Json_files", "eu_country_acronym.json")))

    electricity_ghg_fuel_costs_per_country = json.load(
        open(os.path.join(script_dir, "Json_files", "electricity_ghg_fuel_costs_per_country.json")))

    # get_interest_rate ?


    return {
        "building_properties": building_properties,
        "equipment_details": equipment_details,
        "medium_list": medium_list,
        "fuel_properties": fuel_properties,
        "eu_country_acronym": eu_country_acronym,
        'electricity_ghg_fuel_costs_per_country': electricity_ghg_fuel_costs_per_country
    }


kb = load_db()
