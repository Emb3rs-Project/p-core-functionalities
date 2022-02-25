import json
import os


def load_db():
    script_dir = os.path.dirname(__file__)
    building_properties = json.load(
        os.path.join(script_dir, "Json_files", "building_properties.json")
    )
    equipment_details = json.load(
        os.path.join(script_dir, "Json_files", "equipment_details.json")
    )
    flowrate_to_power = os.path.join(script_dir, "Json_files", "equipment_details.json")
    fluid_material = os.path.join(script_dir, "Json_files", "medium_list.json")
    fuel_properties = os.path.join(script_dir, "Json_files", "eu_country_acronym.json")
    # get_interest_rate ?
    hx_type_and_u = os.path.join(script_dir, "Json_files", "medium_list.json")

    return {
        "building_properties": building_properties,
        "equipment_details": equipment_details,
        "flowrate_to_power": flowrate_to_power,
        "fluid_material": fluid_material,
        "fuel_properties": fuel_properties,
        "hx_type_and_u": hx_type_and_u,
    }


kb = load_db()
