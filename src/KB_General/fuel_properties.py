"""
alisboa/jmcunha


##############################
INFO: The fuel properties are returned according to the country and consumer type (leads to price differences).


##############################
INPUT:
        # country - country name
        # fuel_type - e.g. 'natural_gas', 'fuel_oil', ' biomass', 'electricity'
        # consumer_type - e.g. 'non-household', 'household'


##############################
OUTPUT: dictionary fuel_data, with the following keys:

        # price  [€/kWh]
        # lhv_fuel  [kWh/kg]
        # excess_air_fuel
        # air_to_fuel_ratio  [kg air/kg fuel]
        # co2_emissions  [kg CO2/kWh]
        # density  [kg/m3]


"""

import urllib3
from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.request import urlopen
import json
import ssl


@dataclass
class FuelProperties:
    kb_data: dict

    def get_values(self, country, fuel_type, consumer_type="non-household"):
        """ Get fuel properties

        The fuel properties are returned according to the country and consumer type (leads to price differences).

        Parameters
        ----------
        country : str
            Location country

        fuel_type : str
            Fuel name

        consumer_type : str
            Consumer type

        Returns
        -------
        fuel_data : dict
            Fuel properties: price, lhv_fuel, excess_air_fuel, air_to_fuel_ratio, co2_emissions, density

        """
        context = ssl._create_unverified_context()

        # get KB data
        data_eu_countries = self.kb_data.get('eu_country_acronym')
        data_electricity_ghg_and_fuel_cost_per_country = self.kb_data.get(
            'electricity_ghg_fuel_costs_per_country')
        data_fuel_properties = self.kb_data.get('fuel_properties')

        # get country acronym
        try:
            country_acronyms = data_eu_countries[country]
        except:
            country_acronyms = data_eu_countries['Portugal']

        # get price
        if consumer_type == 'non-household':
            consumer_type = '1'  # Non Household
        else:
            consumer_type = '0'  # Household


        urlelec = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00117/?time=2021&geo='
        urlgas = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00118/?time=2021&geo='
        urlelec = urlelec + country_acronyms
        urlgas = urlgas + country_acronyms

        if fuel_type == 'electricity':
            try:
                info = json.loads(BeautifulSoup(
                    urlopen(urlelec, context=context), "html.parser").text)
                price = info['value'][consumer_type]  # [€/kWh]
            except:
                try:
                    country_acronyms = "EU27_2020"
                    urlelec = urlelec + country_acronyms
                    info = json.loads(BeautifulSoup(
                        urlopen(urlelec, context=context), "html.parser").text)
                    price = info['value'][consumer_type]  # [€/kWh]
                except:
                    price = 0.23  # [€/kWh]

        elif fuel_type == "natural_gas":
            try:
                info = json.loads(BeautifulSoup(
                    urlopen(urlgas, context=context), "html.parser").text)
                price = info['value'][consumer_type] / 277.78  # [€/kWh]
            except:
                try:
                    country_acronyms = "EU27_2020"
                    urlgas = urlgas + country_acronyms
                    info = json.loads(BeautifulSoup(
                        urlopen(urlgas, context=context), "html.parser").text)
                    price = info['value'][consumer_type] / 277.78  # [€/kWh]
                except:
                    price = 0.065  # [€/kWh]


        else:
            fuel_type_cost = fuel_type + '_cost'
            try:
                price = float(
                    data_electricity_ghg_and_fuel_cost_per_country[country][fuel_type_cost])  # [€/kWh]

            except:
                price = float(
                    data_electricity_ghg_and_fuel_cost_per_country['Portugal'][fuel_type_cost])  # [€/kWh]

        # get properties
        if fuel_type == 'natural_gas' or fuel_type == 'biomass' or fuel_type == 'fuel_oil':
            density = float(data_fuel_properties[fuel_type]['density'])
            lhv_fuel = float(
                data_fuel_properties[fuel_type]['lhv'])  # [kWh/kg]
            excess_air_fuel = (float(data_fuel_properties[fuel_type]['excess_air_ratio_min']) + float(
                data_fuel_properties[fuel_type]['excess_air_ratio_max'])) / 2  # average
            air_to_fuel_ratio = float(
                data_fuel_properties[fuel_type]['air_to_fuel_ratio'])
            co2_emissions = float(
                data_fuel_properties[fuel_type]['co2_emissions'])  # [kg/kWh]
            lhv_fuel = lhv_fuel / density

        elif fuel_type == 'electricity':
            density = 'none'
            lhv_fuel = 'none'
            excess_air_fuel = 'none'
            air_to_fuel_ratio = 'none'

            try:
                co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country[country]['electricity_emissions']) \
                    / 1000  # [kg CO2/kW]
            except:
                co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country['Portugal'][
                    'electricity_emissions']) / 1000  # [kg CO2/kW]

        else:
            raise Exception("Fuel data not in the Knowledge Base.")

        fuel_data = {
            'price': price,  # [€/kWh]
            'lhv_fuel': lhv_fuel,  # [kWh/kg]
            'excess_air_fuel': excess_air_fuel,  #
            'air_to_fuel_ratio': air_to_fuel_ratio,  # [kg air/kg fuel]
            'co2_emissions': co2_emissions,  # [kg CO2/kWh]
            'density': density  # [kg/m3]
        }

        return fuel_data
