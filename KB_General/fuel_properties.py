"""
Info: Fuel data
"""

import urllib3
from bs4 import BeautifulSoup
import json
import os

def fuel_properties(country,fuel_type,consumer_type):

    # init arrays
    price = 'none'
    density = 'none'
    lhv_fuel = 'none'  # [kWh/kg]
    excess_air_fuel = 'none'  # average
    air_to_fuel_ratio = 'none'
    co2_emissions = 'none'  # [kg/kWh]

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","eu_country_acronym.json" )


    with abs_file_path as f:
        data_eu_countries = json.load(f)

    try:
        country_acronyms = data_eu_countries[country]
    except:
        country_acronyms = data_eu_countries['Portugal']


    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","electricity_ghg_and_fuel_cost_per_country.json" )

    with abs_file_path as f:
        data_electricity_ghg_and_fuel_cost_per_country = json.load(f)


    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","fuel_properties.json" )

    with abs_file_path as f:
        data_fuel_properties = json.load(f)

    ######
    # get price
    # example: country = 'PT'

    if consumer_type == 'non_household':
        consumer_type = '1'  # Non Household
    else:
        consumer_type = '0'  # Household

    urlelec = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00117/?time=2019&geo='
    urlgas = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00118/?time=2019&geo='
    urlelec = urlelec + country_acronyms
    urlgas = urlgas + country_acronyms

    if fuel_type == 'electricity':
        info = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', urlelec).data, "html.parser").text)
        price = info['value'][consumer_type]  # [€/kWh]

    elif fuel_type == "natural_gas":
        info = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', urlgas).data, "html.parser").text)
        price = info['value'][consumer_type]/277.78  # [€/kWh]

    else:
        try:
            price = float(data_electricity_ghg_and_fuel_cost_per_country[country][fuel_type])  # [€/kWh]
        except:
            price = float(data_electricity_ghg_and_fuel_cost_per_country['Portugal'][fuel_type])  # [€/kWh]
            print('country or fuel does not exist in db')

    ######
    # get properties
    if fuel_type == 'natural_gas' or fuel_type == 'biomass' or fuel_type == 'fuel_oil':
        density = float(data_fuel_properties[fuel_type]['density'])
        lhv_fuel = float(data_fuel_properties[fuel_type]['lhv_fuel'])  # [kWh/kg]
        excess_air_fuel = (float(data_fuel_properties[fuel_type]['excess_air_ratio_min']) + float(data_fuel_properties[fuel_type]['excess_air_ratio_max']))/2  # average
        air_to_fuel_ratio = float(data_fuel_properties[fuel_type]['air_to_fuel_ratio'])
        co2_emissions = float(data_fuel_properties[fuel_type]['co2_emissions'])  # [kg/kWh]

    elif fuel_type == 'electricity':
        density = 'none'
        lhv_fuel = 'none'
        excess_air_fuel = 'none'
        air_to_fuel_ratio = 'none'

        try:
            co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country[country]['electricity_emissions']) / 1000  # [kg CO2/kW]
        except:
            co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country['Portugal']['electricity_emissions']) / 1000  # [kg CO2/kW]
            print('country does not exist in db')

    else:
        print('Fuel does not exist in database')

    output ={
        'price': price ,    # [€/kWh]
        'lhv_fuel': lhv_fuel,  # [kWh/kg]
        'excess_air_fuel': excess_air_fuel, #
        'air_to_fuel_ratio': air_to_fuel_ratio, # [kg air/kg fuel]
        'co2_emissions': co2_emissions, # [kg CO2/kWh]
        'density': density  # [kg/m3]
        }

    return output
