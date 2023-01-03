from ast import literal_eval
from enum import Enum
from typing import Optional

from pydantic import PositiveFloat, StrictStr, root_validator, validator

from .reference_system import ReferenceSystem
from ..General.error_adjust_capacity import AdjustCapacity


class ScheduleInfo(int, Enum):
    off = 0
    on = 1


class SimpleIndustryStreamDataInput(ReferenceSystem, AdjustCapacity):
    name: str
    supply_temperature: PositiveFloat
    target_temperature: PositiveFloat
    fluid: StrictStr
    fluid_cp: Optional[PositiveFloat]
    flowrate: Optional[PositiveFloat]
    daily_periods: Optional[str]
    shutdown_periods: Optional[str]
    saturday_on: Optional[ScheduleInfo]
    sunday_on: Optional[ScheduleInfo]

    monday_daily_periods: Optional[StrictStr]
    tuesday_daily_periods: Optional[StrictStr]
    wednesday_daily_periods: Optional[StrictStr]
    thursday_daily_periods: Optional[StrictStr]
    friday_daily_periods: Optional[StrictStr]
    saturday_daily_periods: Optional[StrictStr]
    sunday_daily_periods: Optional[StrictStr]

    capacity: Optional[PositiveFloat] = None

    @validator("target_temperature", allow_reuse=True)
    def check_if_temperatures_are_the_same(cls, target_temperature, values, **kwargs):
        if target_temperature == values["supply_temperature"]:
            raise Exception("Stream supply and target temperature must be different")
        return target_temperature

    @validator(
        "daily_periods",
        "monday_daily_periods",
        "tuesday_daily_periods",
        "wednesday_daily_periods",
        "thursday_daily_periods",
        "friday_daily_periods",
        "saturday_daily_periods",
        "sunday_daily_periods",
    )
    def check_structure_daily_periods(cls, daily_periods):
        daily_periods = literal_eval(daily_periods) if daily_periods else []
        if not isinstance(daily_periods, list):
            raise TypeError("Provide a list for daily periods.")

        for period in daily_periods:
            if len(period) != 2:
                raise ValueError(
                    "Only a start and ending hour must be given in each daily period. Example: [[9,12],[14,19]]"
                )

            period_a, period_b = period
            if period_b <= period_a:
                raise ValueError(
                    "Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]"
                )

        return daily_periods

    @validator("shutdown_periods")
    def check_structure_shutdown_periods(cls, shutdown_periods):
        shutdown_periods = literal_eval(shutdown_periods) if shutdown_periods else []
        if not isinstance(shutdown_periods, list):
            raise TypeError("Provide a list for shutdown periods.")

        for period in shutdown_periods:
            if len(period) != 2:
                raise ValueError(
                    "Only a start and ending day must be given in each shutdown period. Example: [[220,250]]"
                )

            period_a, period_b = period
            if period_b <= period_a:
                raise ValueError(
                    "Second value of the shutdown period must be larger than the first. Example: [[220,250]]"
                )

        return shutdown_periods

    @validator('capacity', always=True)
    def check_capacity_or_flowrate_and_cp(cls, capacity, values, **kwargs):
        if values["fluid"] == 'steam' and capacity == None:
            raise Exception('When introducing steam as a fluid, introduce the capacity.')
        elif (capacity == None and values['flowrate'] == None and values['fluid_cp'] == None):
            raise Exception('To characterize a stream, introduce Capacity or Mass Flowrate and Cp.')
        elif (capacity == None and (values['flowrate'] == None or values['fluid_cp'] == None)):
            raise Exception('To characterize a stream, introduce Capacity or Mass Flowrate and Cp.')
        elif (capacity != None and values['flowrate'] != None and values['fluid_cp'] != None):
            raise Exception('To characterize a stream, introduce Capacity or Mass Flowrate and Cp.')
        else:
            return capacity

    @root_validator
    def check_if_generated_or_import_schedule(cls, values):
        try:
            real_hourly_capacity = values["real_hourly_capacity"]
            daily_periods = values["daily_periods"]
            shutdown_periods = values["shutdown_periods"]
            saturday_on = values["saturday_on"]
            sunday_on = values["sunday_on"]
        except KeyError:
            # When a key does not exist in 'values' is an indicator that related attribute has an error,
            # so bellow return will skip this validation and gives the responsibility of exception to Pydantic
            return values

        all_has_value = None not in (daily_periods, shutdown_periods, saturday_on, sunday_on)

        if not real_hourly_capacity and not all_has_value:
            raise Exception("Import a profile (kWh) for the stream or provide data to estimate one.")

        if real_hourly_capacity and all_has_value:
            raise Exception("Provide only the profile (kWh), or the schedule data, not both.")

        return values
