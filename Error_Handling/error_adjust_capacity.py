from pydantic import BaseModel, NonNegativeFloat, validator, PositiveFloat, StrictStr, conlist
from typing import Optional, Dict
from enum import Enum

class StreamType(str, Enum):
    inflow = 'inflow'

class StreamBuilding(BaseModel):
    id: int
    object_type: str
    stream_type: StreamType
    supply_temperature: PositiveFloat
    target_temperature: PositiveFloat
    fluid: StrictStr
    schedule: conlist(int)
    hourly_generation: conlist(NonNegativeFloat)
    monthly_generation: conlist(NonNegativeFloat,min_items=12,max_items=12)
    capacity: PositiveFloat

    object_id: Optional[float]

class UserMonthlyCapacity(BaseModel):
    january: Optional[NonNegativeFloat]
    february: Optional[NonNegativeFloat]
    march: Optional[NonNegativeFloat]
    april: Optional[NonNegativeFloat]
    may: Optional[NonNegativeFloat]
    june: Optional[NonNegativeFloat]
    july: Optional[NonNegativeFloat]
    august: Optional[NonNegativeFloat]
    september: Optional[NonNegativeFloat]
    october: Optional[NonNegativeFloat]
    november: Optional[NonNegativeFloat]
    december: Optional[NonNegativeFloat]


class PlatformAdjustCapacity(BaseModel):

    stream: StreamBuilding
    user_monthly_capacity: Optional[UserMonthlyCapacity]
    user_yearly_capacity: Optional[NonNegativeFloat]

    @validator("user_yearly_capacity", always=True)
    def check_which_capacity_was_given(cls, user_yearly_capacity, values, **kwargs):


        if values["user_monthly_capacity"] is None and user_yearly_capacity is None:
            raise Exception('To adjust capacities, provide real monthly or yearly capacities.')

        elif values["user_monthly_capacity"] is not None and user_yearly_capacity is not None:
            raise Exception('To adjust capacities provide, only real monthly capacities or yearly capacity.')

        else:
            return user_yearly_capacity





