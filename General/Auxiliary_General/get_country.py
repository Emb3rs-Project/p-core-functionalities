from geopy.geocoders import Nominatim

def get_country(latitude,longitude):

    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(latitude) + "," + str(longitude), language='en')
        address = location.raw['address']
        country = str(address.get('country'))


    except:
        country = 'Portugal'



    return country

