"""
alisboa/jmcunha


##############################
INFO: get country name by introducing location coordinates

##############################
INPUT:
        # latitude  [º]
        # longitude  [º]


##############################
RETURN:
        # country


"""

from geopy.geocoders import Nominatim


def get_country(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(latitude) + "," + str(longitude), language='en')
        address = location.raw['address']
        country = str(address.get('country'))


    except:
        country = 'Portugal'

    return country
