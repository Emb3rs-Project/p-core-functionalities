"""
Info: Fuel data
"""

import urllib3
from bs4 import BeautifulSoup
import json

def fuel_properties(country,fuel_type,consumer_type):

    # init arrays
    price = 'none'
    density = 'none'
    lhv_fuel = 'none'  # [kWh/kg]
    excess_air_fuel = 'none'  # average
    AFR_fuel = 'none'
    CO2_emission = 'none'  # [kg/kWh]


    with open(
            'C:/Users/alisboa/PycharmProjects/emb3rs/KB_General/Json_files/eu_country_acronym.json') as f:
        data_eu_countries = json.load(f)

    try:
        country_acronyms = data_eu_countries[country]
    except:
        country_acronyms = data_eu_countries['Portugal']


    with open(
            'C:/Users/alisboa/PycharmProjects/emb3rs/KB_General/Json_files/electricity_ghg_and_fuel_cost_per_country.json') as f:
        data_electricity_ghg_and_fuel_cost_per_country = json.load(f)

    with open('C:/Users/alisboa/PycharmProjects/emb3rs/KB_General/Json_files/fuel_properties.json') as f:
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

    elif fuel_type == "biomass":
        price = 15  # [€/kWh]

    else:
        for dict in data_electricity_ghg_and_fuel_cost_per_country['electricity_ghg_and_fuel_cost_per_country']:
            if dict['country'] == country:
                price = float(dict[fuel_type])  # [€/kWh]
                break
            else:
                price = float(data_electricity_ghg_and_fuel_cost_per_country['electricity_ghg_and_fuel_cost_per_country'][0][fuel_type])  # [€/kWh]


    ######
    # get properties
    if fuel_type == 'natural_gas' or fuel_type == 'biomass' or fuel_type == 'fuel_oil':
        density = float(data_fuel_properties['fuel_properties'][0][fuel_type])
        lhv_fuel = float(data_fuel_properties['fuel_properties'][1][fuel_type])  # [kWh/kg]
        excess_air_fuel = (float(data_fuel_properties['fuel_properties'][6][fuel_type]) + float(data_fuel_properties['fuel_properties'][7][fuel_type]))/2 # average
        AFR_fuel = float(data_fuel_properties['fuel_properties'][5][fuel_type])
        CO2_emission = float(data_fuel_properties['fuel_properties'][3][fuel_type] ) # [kg/kWh]

    elif fuel_type == 'electricity':
        density = 'none'
        lhv_fuel = 'none'
        excess_air_fuel = 'none'
        AFR_fuel = 'none'

        for dict in data_electricity_ghg_and_fuel_cost_per_country['electricity_ghg_and_fuel_cost_per_country']:
            if dict['country'] == country:
                CO2_emission = float(dict['electricity_emissions']) / 1000  # [kg CO2/kW]
                break
            else:
                CO2_emission = float(data_electricity_ghg_and_fuel_cost_per_country['electricity_ghg_and_fuel_cost_per_country'][0][
                    'electricity_emissions']) / 1000  # [kg CO2/kW]


    else:
        print('Fuel does not exist in database')



    output ={
        'price': price ,    # [€/kWh]
        'lhv_fuel': lhv_fuel,  # [kWh/kg]
        'excess_air_fuel': excess_air_fuel, #
        'AFR_fuel': AFR_fuel, # [kg air/kg fuel]
        'CO2_emission': CO2_emission, # [kg CO2/kWh]
        'density': density  # [kg/m3]
        }

    return output

