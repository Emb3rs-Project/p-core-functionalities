from pydantic import BaseModel, validator, conlist


class Location(BaseModel):
    location: conlist(float, min_items=2, max_items=2)

    @validator('location')
    def check_location(cls, location):

        latitude, longitude = location

        if not -90 <= latitude <= 90:
            raise ValueError('latitude must be within [-90,90]. location = [latitude,longitude]')

        if not -180 <= longitude <= 180:
            raise ValueError('longitude must be within [-180,180]. location = [latitude,longitude]')

        return location
