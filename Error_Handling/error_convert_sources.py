from pydantic import BaseModel, validator, PositiveFloat
from typing import List, Optional
from .source_or_sink import SourceOrSink
from .gis_source_losses import GISSourceLosses

class PlatformConvertSources(BaseModel):

    group_of_sources: List[SourceOrSink]

    @validator('group_of_sources')
    def check_if_there_are_sources(cls, v):
        if len(v) < 1:
           raise ValueError('Introduce at least 1 source')
        return v


class GISConvertSources(BaseModel):

    sources_losses: Optional[List[GISSourceLosses]]


class CFConvertSources(BaseModel):

    sink_group_grid_return_temperature: PositiveFloat
    sink_group_grid_supply_temperature: PositiveFloat

    @validator('sink_group_grid_supply_temperature')
    def check_grid_temperatures(cls, v, values, **kwargs):
        if v < values['sink_group_grid_return_temperature']:
           raise ValueError('Grid supply temperature must be larger than the return temperature.'
                            ' sink_group_grid_supply_temperature>sink_group_grid_return_temperature')
        return v