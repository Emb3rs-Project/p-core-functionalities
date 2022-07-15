from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.request import urlopen
import json
import ssl
from module.General.Auxiliary_General.get_country import get_country


@dataclass
class FuelProperties:
    kb_data: dict

    def get_values(self, location):

        latitude, longitude = location
        country = get_country(latitude, longitude)

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
        consumer_type = '1'  # NON - Household

        urlelec = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00117/?time=2021&geo='
        urlgas = 'https://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/ten00118/?time=2021&geo='
        urlelec = urlelec + country_acronyms
        urlgas = urlgas + country_acronyms

        try:
            info = json.loads(BeautifulSoup(
                urlopen(urlelec, context=context), "html.parser").text)
            elec_price = info['value'][consumer_type]  # [€/kWh]
        except:
            try:
                country_acronyms = "EU27_2020"
                urlelec = urlelec + country_acronyms
                info = json.loads(BeautifulSoup(
                    urlopen(urlelec, context=context), "html.parser").text)
                elec_price = info['value'][consumer_type]  # [€/kWh]
            except:
                elec_price = 0.23  # [€/kWh]


        try:
            info = json.loads(BeautifulSoup(
                urlopen(urlgas, context=context), "html.parser").text)
            ng_price = info['value'][consumer_type] / 277.78  # [€/kWh]
        except:
            try:
                country_acronyms = "EU27_2020"
                urlgas = urlgas + country_acronyms
                info = json.loads(BeautifulSoup(
                    urlopen(urlgas, context=context), "html.parser").text)
                ng_price = info['value'][consumer_type] / 277.78  # [€/kWh]
            except:
                ng_price = 0.065  # [€/kWh]


        try:
            bio_price = float(
                data_electricity_ghg_and_fuel_cost_per_country[country]['biomass_cost'])  # [€/kWh]
        except:
            bio_price = float(
                data_electricity_ghg_and_fuel_cost_per_country['Portugal']['biomass_cost'])  # [€/kWh]

        try:
            fo_price = float(
                data_electricity_ghg_and_fuel_cost_per_country[country]['fuel_oil_cost'])  # [€/kWh]
        except:
            fo_price = float(
                data_electricity_ghg_and_fuel_cost_per_country['Portugal']['fuel_oil_cost'])  # [€/kWh]


        # get properties
        ng_co2_emissions = float(
            data_fuel_properties["natural_gas"]['co2_emissions'])  # [kg/kWh]
        bio_co2_emissions = float(
            data_fuel_properties["biomass"]['co2_emissions'])  # [kg/kWh]
        fo_co2_emissions = float(
            data_fuel_properties["fuel_oil"]['co2_emissions'])  # [kg/kWh]



        try:
            elec_co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country[country]['electricity_emissions']) \
                / 1000  # [kg CO2/kW]
        except:
            elec_co2_emissions = float(data_electricity_ghg_and_fuel_cost_per_country['Portugal'][
                'electricity_emissions']) / 1000  # [kg CO2/kW]


        fuels_data = {
            "fuels_data": {
                "natural_gas": {
                    "co2_emissions": ng_co2_emissions,
                    "price": ng_price},
                "biomass": {
                    "co2_emissions": bio_co2_emissions,
                    "price": bio_price},
                "fuel_oil": {
                    "co2_emissions": fo_co2_emissions,
                    "price": fo_price},
                "electricity": {
                    "co2_emissions": elec_co2_emissions,
                    "price": elec_price}
            }}
        return fuels_data