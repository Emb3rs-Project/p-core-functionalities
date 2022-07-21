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

class FuelChoices(str, Enum):
    electricity = "electricity"
    natural_gas = "natural_gas"
    biomass = "biomass"
    fuel_oil = "fuel_oil"
    none = "none"

class Stream(BaseModel):
    id: int
    name: Optional[str]
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
    fuel: Optional[FuelChoices] = "none"
    eff_equipment: Union[PositiveFloat, None]

    @validator('schedule', allow_reuse=True)
    def check_if_valid_values(cls, v):
        _v = list(filter(lambda num: num != 0, v))
        _v = list(filter(lambda num: num != 1, _v))

        if len(_v) > 0:
            raise ValueError('Values not valid found (only 0 or 1)')
        return v
