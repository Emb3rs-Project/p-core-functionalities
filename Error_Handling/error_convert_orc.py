from pydantic import validator, PositiveInt, PositiveFloat
from typing import List, Optional
from .General.stream import Stream
from .General.location import Location
from .General.consumer_type_options import ConsumerTypeOptions
from .General.fueldata import FuelData

class PlatformConvertORC(Location):
    streams: List[Stream]
    get_best_number: Optional[PositiveInt] = 3
    orc_years_working: Optional[PositiveInt] = 25
    orc_T_evap: Optional[PositiveFloat] = 110
    orc_T_cond: Optional[PositiveFloat] = 35
    fuels_data: FuelData
    interest_rate: Optional[PositiveFloat] = 0.04

    @validator('streams')
    def check_if_there_are_streams(cls, v):
        if len(v) < 1:
            raise ValueError('Introduce at least 1 stream to assess a possible ORC.')
        return v

    @validator('orc_T_cond')
    def check_orc_temperatures(cls, orc_T_cond, values, **kwargs):
        if orc_T_cond >= values['orc_T_evap']:
            raise ValueError('ORC Evaporator temperature must be larger than the Condenser temperature')

        return orc_T_cond
