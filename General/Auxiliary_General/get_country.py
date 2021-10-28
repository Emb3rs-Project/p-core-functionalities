import urllib3
from bs4 import BeautifulSoup
import json

def get_country(latitude,longitude):

    try:
        urlcountr = 'https://nominatim.openstreetmap.org/reverse.php?format=json&3153965&accept-language=en'
        urlcountry = urlcountr + '&lat=' + str(latitude) + '&lon=' + str(longitude)
        urlcountry = json.loads(BeautifulSoup(urllib3.PoolManager().request('GET', urlcountry).data, "html.parser").text)
        country = urlcountry['address']['country']

    except:
        country = 'Portugal'

    return country

