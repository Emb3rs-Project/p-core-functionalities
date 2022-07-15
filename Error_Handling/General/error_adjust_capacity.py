"""
alisboa/jmcunha


##############################
INFO: Adjust capacity error handling


"""

from pydantic import BaseModel, NonNegativeFloat, validator, PositiveFloat, StrictStr, conlist
from typing import Optional, Union
from enum import Enum


class MonthlyCapacity(BaseModel):
    january: NonNegativeFloat
    february: NonNegativeFloat
    march: NonNegativeFloat
    april: NonNegativeFloat
    may: NonNegativeFloat
    june: NonNegativeFloat
    july: NonNegativeFloat
    august: NonNegativeFloat
    september: NonNegativeFloat
    october: NonNegativeFloat
    november: NonNegativeFloat
    december: NonNegativeFloat


class AdjustCapacity(BaseModel):
    real_hourly_capacity: Optional[conlist(NonNegativeFloat, min_items=8760, max_items=8760)] = None
    real_daily_capacity: Optional[conlist(NonNegativeFloat, min_items=365, max_items=366)] = None
    real_monthly_capacity: Optional[MonthlyCapacity] = None
    real_yearly_capacity: Optional[NonNegativeFloat] = None

    @validator("real_hourly_capacity", "real_daily_capacity", "real_monthly_capacity","real_yearly_capacity", allow_reuse=True)
    def check_if_more_than_one_parameter_is_given(cls, actual_parameter, values, **kwargs):

        boolean_list = []
        boolean_list.append(actual_parameter is not None)
        for key in values.keys():
            boolean_list.append(values[key] is not None)

        if boolean_list.count(True) > 1:
            raise Exception(
                "Provide only one real profile for your stream (daily,monthly or yearly - never more than one)")

        return actual_parameter