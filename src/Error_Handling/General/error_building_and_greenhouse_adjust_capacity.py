from pydantic import BaseModel, NonNegativeFloat, validator, conlist
from typing import Optional




class BuildingandGreenhouseAdjustCapacity(BaseModel):

    real_heating_monthly_capacity: Optional[conlist(NonNegativeFloat, min_items=12, max_items=12)] = None
    real_heating_yearly_capacity: Optional[NonNegativeFloat] = None
    real_cooling_monthly_capacity: Optional[conlist(NonNegativeFloat, min_items=12, max_items=12)] = None
    real_cooling_yearly_capacity: Optional[NonNegativeFloat] = None

    @validator("real_heating_monthly_capacity", "real_heating_yearly_capacity", allow_reuse=True)
    def check_if_more_than_one_parameter_is_given_heating(cls, actual_parameter, values, **kwargs):
        boolean_list = []
        boolean_list.append(actual_parameter is not None)
        for key in values.keys():
            if key == "real_heating_monthly_capacity" or key == "real_heating_yearly_capacity":
                boolean_list.append(values[key] is not None)

        if boolean_list.count(True) > 1:
            raise Exception(
                "Provide only one real profile for your stream (daily,monthly or yearly - never more than one)")

        return actual_parameter    \

    @validator("real_cooling_monthly_capacity", "real_cooling_yearly_capacity", allow_reuse=True)
    def check_if_more_than_one_parameter_is_given_cooling(cls, actual_parameter, values, **kwargs):
        boolean_list = []
        boolean_list.append(actual_parameter is not None)

        for key in values.keys():
            if key == "real_cooling_monthly_capacity" or key == "real_cooling_yearly_capacity":
                boolean_list.append(values[key] is not None)

        if boolean_list.count(True) > 1:
            raise Exception(
                "Provide only one real profile for your stream (daily,monthly or yearly - never more than one)")

        return actual_parameter