"""
##############################
INFO: Get interest rate of a country for the most recent year in EUROSTAT.
      If the interest rate is not found in the API for a specific country, the script returns Portugal's interest rate.

##############################
INPUT:
        # country - country name

##############################
OUTPUT:
        # interest_rate  []

"""

import requests
import ast
import os
import json

def get_interest_rate(country):

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, "Json_files","eu_country_acronym.json" )

    with open(abs_file_path) as f:
        data_eu_countries = json.load(f)

    # get country acronym
    try:
        country_acronym = data_eu_countries[country]
    except:
        country_acronym = data_eu_countries['Portugal']


    # get data
    url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/IRT_LT_MCBY_A?format=JSON&lang=en&freq=A&int_rt=MCBY&geo=EU27_2020&geo=EU28&geo=EA&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&geo=UK&time=2011&time=2012&time=2013&time=2014&time=2015&time=2016&time=2017&time=2018&time=2019&time=2020'
    html = requests.get(url).content
    dict_str = html.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    # get country's interest rate
    get_country_index = int(mydata['dimension']['geo']['category']['index'][country_acronym]) + 1
    number_years = len(mydata['dimension']['time']['category']['label'])
    index_interest_rate = str(number_years * get_country_index - 1)

    try:
        interest_rate = mydata['value'][index_interest_rate]

    except:
        get_country_index = int(mydata['dimension']['geo']['category']['index']['PT']) + 1
        number_years = len(mydata['dimension']['time']['category']['label'])
        index_interest_rate = str(number_years * get_country_index - 1)
        interest_rate = mydata['value'][index_interest_rate]


    return interest_rate

