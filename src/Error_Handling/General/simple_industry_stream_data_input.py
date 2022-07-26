from pydantic import validator, PositiveFloat, StrictStr
from typing import Optional
from enum import Enum
import ast
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
    capacity: Optional[PositiveFloat] = None

    @validator('daily_periods')
    def check_structure_daily_periods(cls, daily_periods):
        daily_periods = ast.literal_eval(daily_periods)
        if daily_periods != []:
            if isinstance(daily_periods, list) is True:
                for period in daily_periods:
                    if len(period) != 2:
                        raise ValueError(
                            'Only a start and ending hour must be given in each daily period. Example: [[9,12],[14,19]]')
                    else:
                        period_a, period_b = period
                        if period_b <= period_a:
                            raise ValueError(
                                'Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]')
            else:
                raise TypeError('Provide a list for daily periods.')
        else:
            raise TypeError('Provide daily periods in the correct format. Example: [[11,20]] or [[9,12],[14,19]]')

        return daily_periods

    @validator('shutdown_periods')
    def check_structure_shutdown_periods(cls, shutdown_periods):

        shutdown_periods = ast.literal_eval(shutdown_periods)
        if shutdown_periods != []:
            if isinstance(shutdown_periods, list) is True:
                for period in shutdown_periods:
                    if len(period) != 2:
                        raise ValueError(
                            'Only a start and ending day must be given in each shutdown period. Example: [[220,250]]')
                    else:
                        period_a, period_b = period
                        if period_b <= period_a:
                            raise ValueError(
                                'Second value of the shutdown period must be larger than the first. Example: [[220,250]]')
            else:
                raise TypeError(
                    'Provide a list for shutdown periods.')

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

    @validator('real_hourly_capacity')
    def check_if_generated_or_import_schedule(cls, real_hourly_capacity, values, **kwargs):

        if real_hourly_capacity is None:
            if values["daily_periods"] is None or values["shutdown_periods"] is None or values["saturday_on"] is None or values["sunday_on"] is None:
                raise Exception("Import a profile (kWh) for the stream or provide data to estimate one.")
        else:
            if values["daily_periods"] is not None or values["shutdown_periods"] is not None or values["saturday_on"] is not None or values["sunday_on"] is not None:
                raise Exception("Provide only the profile (kWh), or the schedule data, not both.")

        return real_hourly_capacity

    @validator('target_temperature',allow_reuse=True)
    def check_if_temperatures_are_the_same(cls, target_temperature, values, **kwargs):

        if target_temperature == values["supply_temperature"]:
            raise Exception("Stream supply and target temperature must be different")


        return target_temperature

