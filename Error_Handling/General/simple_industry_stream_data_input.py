from pydantic import BaseModel, validator, conint, conlist, PositiveFloat, StrictStr, NonNegativeFloat
from typing import Optional
from enum import Enum


class ScheduleInfo(int, Enum):
    off = 0
    on = 1


class SimpleIndustryStreamDataInput(BaseModel):

    supply_temperature: PositiveFloat
    target_temperature: PositiveFloat
    fluid: StrictStr
    fluid_cp: PositiveFloat

    flowrate: Optional[PositiveFloat]

    daily_periods: Optional[conlist(conlist(conint(ge=0, le=24), min_items=2, max_items=2), min_items=0)]
    shutdown_periods: Optional[conlist(conlist(conint(ge=0, le=365), min_items=2, max_items=2), min_items=0)]
    saturday_on: Optional[ScheduleInfo]
    sunday_on: Optional[ScheduleInfo]

    capacity: Optional[PositiveFloat] = None
    hourly_generation: Optional[conlist(NonNegativeFloat, min_items=8760, max_items=8760)]


    @validator('hourly_generation', always=True)
    def check_if_generated_or_import_schedule(cls, hourly_generation_profile, values,**kwargs):
        if hourly_generation_profile is None:
            if values["daily_periods"] is None or values["shutdown_periods"] is None or values["saturday_on"] is None or values["sunday_on"] is None:
                raise Exception("Import a profile (kWh) for the stream or provide data to estimate one.")
        else:
            if values["daily_periods"] is not None or values["shutdown_periods"] is not None or values["saturday_on"] is not None or values["sunday_on"] is not None:
                raise Exception("Provide only the profile (kWh), or the schedule data, not both.")

        return hourly_generation_profile


    @validator('daily_periods')
    def check_structure_daily_periods(cls, v):

        if v != []:
            for value in v:
                if len(value) != 2:
                    raise ValueError(
                        'Only a start and ending hour must be given in each period. Example: [[9,12],[14,19]]')
                else:
                    value_a, value_b = value
                    if value_b <= value_a:
                        raise ValueError(
                            'Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]')

        return v

    @validator('shutdown_periods')
    def check_structure_shutdown_periods(cls, v):
        if v != []:
            for value in v:
                if len(value) != 2:
                    raise ValueError('Only a start and ending day must be given in each period. Example: [[220,250]]')
                else:
                    value_a, value_b = value
                    if value_b <= value_a:
                        raise ValueError(
                            'Second value of the shutdown period must be larger than the first. Example: [[220,250]]')
        return v


    @validator('capacity', always=True)
    def give_capacity_for_steam(cls, capacity, values, **kwargs):

        if values["fluid"] == 'steam' and capacity == None:
            raise Exception('When introducing steam as a fluid, introduce the capacity.')
        else:
            return capacity

