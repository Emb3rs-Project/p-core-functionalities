from pydantic import BaseModel, validator
from enum import Enum
import ast


class ScheduleInfo(int, Enum):
    off = 0
    on = 1


class Schedule(BaseModel):
    daily_periods: str
    shutdown_periods: str
    saturday_on: ScheduleInfo
    sunday_on: ScheduleInfo

    @validator('daily_periods')
    def check_structure_daily_periods(cls, daily_periods):
        daily_periods = ast.literal_eval(daily_periods)
        if daily_periods != []:
            if isinstance(daily_periods, list) is True:
                for period in daily_periods:
                    if len(period) != 2:
                        raise ValueError(
                            'Only a start and ending hour must be given in each period. Example: [[9,12],[14,19]]')
                    else:
                        period_a, period_b = period
                        if period_b <= period_a:
                            raise ValueError(
                                'Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]')
            else:
                raise TypeError('Provide a list for daily periods.')

        return daily_periods

    @validator('shutdown_periods')
    def check_structure_shutdown_periods(cls, shutdown_periods):

        shutdown_periods = ast.literal_eval(shutdown_periods)
        if shutdown_periods != []:
            if isinstance(shutdown_periods, list) is True:
                for period in shutdown_periods:
                    if len(period) != 2:
                        raise ValueError(
                            'Only a start and ending day must be given in each period. Example: [[220,250]]')
                    else:
                        period_a, period_b = period
                        if period_b <= period_a:
                            raise ValueError(
                                'Second value of the shutdown period must be larger than the first. Example: [[220,250]]')
            else:
                raise TypeError(
                    'Provide a list for shutdown periods.')

        return shutdown_periods
