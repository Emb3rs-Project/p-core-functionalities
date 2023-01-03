"""
alisboa/jmcunha


##############################
INFO: Adjust capacity error handling


"""
from typing import Optional

from pydantic import BaseModel, NonNegativeFloat, conlist, validator


class AdjustCapacity(BaseModel):
    real_hourly_capacity: Optional[conlist(NonNegativeFloat, min_items=8760, max_items=8760)]
    real_daily_capacity: Optional[conlist(NonNegativeFloat, min_items=365, max_items=366)]
    real_monthly_capacity:  Optional[conlist(NonNegativeFloat, min_items=12, max_items=12)]
    real_yearly_capacity: Optional[NonNegativeFloat]

    @validator(
        "real_hourly_capacity",
        "real_daily_capacity",
        "real_monthly_capacity",
        "real_yearly_capacity",
        allow_reuse=True,
    )
    def check_if_more_than_one_parameter_is_given(cls, actual_parameter, values, **kwargs):
        boolean_list = [actual_parameter is not None]
        boolean_list += [value is not None for value in values.values()]
        if boolean_list.count(True) > 1:
            raise Exception(
                "Provide only one real profile for your stream (daily,monthly or yearly - never more than one)"
            )
        return actual_parameter
