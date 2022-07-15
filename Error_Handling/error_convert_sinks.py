from pydantic import BaseModel, validator, confloat
from typing import List, Optional
from .Convert_Source_Sink.source_or_sink import SourceOrSink


class PlatformConvertSinks(BaseModel):
    group_of_sinks: List[SourceOrSink]
    grid_supply_temperature: Optional[confloat(gt=5, le=110)] = None
    grid_return_temperature: Optional[confloat(gt=5, le=110)] = None

    @validator('group_of_sinks')
    def check_if_there_are_sinks(cls, group_of_sinks):
        if len(group_of_sinks) < 1:
            raise ValueError('Introduce at least 1 sink to assess a possible District Heating Network.')
        return group_of_sinks

    @validator('grid_return_temperature', always=True)
    def check_temperatures(cls, grid_return_temperature, values, **kwargs):

        if grid_return_temperature is None and values['grid_supply_temperature'] is None:
            return grid_return_temperature

        elif (grid_return_temperature is None and values['grid_supply_temperature'] is not None) or (
                grid_return_temperature is not None and values['grid_supply_temperature'] is None):
            raise ('Introduce both, District Heating Network supply and return temperatures, or None.')

        return grid_return_temperature
