from pydantic import BaseModel, validator, conlist, PositiveFloat, NonNegativeFloat, StrictStr
from typing import Optional
from enum import Enum

class StreamType(str, Enum):

    value_1 = 'inflow'
    value_2 = 'outflow'
    value_3 = 'excess_heat'
    value_4 = 'supply_heat'


class Stream(BaseModel):

    id: int
    object_type: str
    stream_type: StreamType
    supply_temperature: PositiveFloat
    target_temperature: PositiveFloat
    fluid: StrictStr
    flowrate: PositiveFloat
    schedule: conlist(int)
    hourly_generation: conlist(NonNegativeFloat)
    capacity: PositiveFloat

    object_id: Optional[float]


    @validator('schedule')
    def check_if_valid_values (cls, v):

        _v = list(filter(lambda num: num != 0, v))
        _v = list(filter(lambda num: num != 1, _v))

        if len(_v) > 0:
            raise ValueError('Values not valid found (only 0 or 1)')
        return v