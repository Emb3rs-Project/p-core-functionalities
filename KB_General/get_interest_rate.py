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
import urllib3
from bs4 import BeautifulSoup
from dataclasses import dataclass
import json
import pandas as pd

def get_interest_rate(country):

    url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/TEIMF050?format=JSON&lang=en'

    try:
        #info = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', url).data, "html.parser").text)
        interest_rate = 0.05
    except:
        interest_rate = 0.05

    return interest_rate

