from pydantic import BaseModel, validator, conlist, PositiveFloat, NonNegativeFloat, StrictStr
from typing import Optional, Union
from enum import Enum

class StreamType(str, Enum):

    inflow = 'inflow'
    outflow = 'outflow'
    excess_heat = 'excess_heat'
    supply_heat = 'supply_heat'
    hot_stream = "hot_stream"
    cold_stream = "cold_stream"


class Stream(BaseModel):

    id: int
    object_type: str
    stream_type: StreamType
    supply_temperature: PositiveFloat
    target_temperature: PositiveFloat
    fluid: StrictStr
    flowrate: Union[PositiveFloat, None]
    schedule: conlist(int)
    hourly_generation: conlist(NonNegativeFloat)
    capacity: PositiveFloat

    object_linked_id: Optional[float] = None


    @validator('schedule')
    def check_if_valid_values (cls, v):

        _v = list(filter(lambda num: num != 0, v))
        _v = list(filter(lambda num: num != 1, _v))

        if len(_v) > 0:
            raise ValueError('Values not valid found (only 0 or 1)')
        return v