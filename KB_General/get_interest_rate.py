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


import urllib3
from bs4 import BeautifulSoup
import json
from ..utilities.kb import KB
from ..KB_General.country_acronym import CountryAcronym
from datetime import datetime

def get_interest_rate(country,kb : KB):

    try:
        country = 'Spain'
        country_acronym = CountryAcronym(kb)
        country_acronym = str(country_acronym.get_values(country))

        currentMonth = datetime.now().month

        if currentMonth == 1:
            currentMonth = '12'
            currentYear = str(datetime.now().year -1)
        else:
            currentMonth = '0' + str(currentMonth-1)
            currentYear = str(datetime.now().year)

        url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/IRT_LT_MCBY_M?format=JSON&lang=en&freq=M&geo=' + country_acronym + '&time=' + currentYear + '-' + currentMonth
        info = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', url).data, "html.parser").text)
        interest_rate = info['value']['0']/100

    except:
        print('Error getting interest rate. Default: 0.02')
        interest_rate = 0.02


    return interest_rate

