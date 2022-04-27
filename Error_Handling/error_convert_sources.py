from pydantic import BaseModel, validator, PositiveFloat, confloat
from typing import List, Optional
from .source_or_sink import SourceOrSink
from .gis_source_losses import GISSourceLosses


class MainErrorConvertSources(BaseModel):

    platform: dict = None
    cf_module: dict = None
    gis_module: Optional[dict]


    @validator("platform","cf_module",always=True)
    def fasd(cls,v):

        if v == None:
            raise Exception(
                'Introduce a dictionary with \'platform\', \'cf_module\' and \'gis_module\' (optional)\', and the correspondent necessary data.')

        return v


    @validator('platform')
    def platform_inputs(cls,v):

        class PlatformConvertSources(BaseModel):

            group_of_sources: List[SourceOrSink]

            @validator('group_of_sources')
            def check_if_there_are_sources(cls, v):
                if len(v) < 1:
                    raise ValueError('Introduce at least 1 source')
                return v

        return(PlatformConvertSources(**v))


    @validator('gis_module')
    def gis_module_inputs(cls, v):

        class GISConvertSources(BaseModel):

            sources_losses: Optional[List[GISSourceLosses]]

        return(GISConvertSources(**v))


    @validator('cf_module')
    def cf_module_inputs(cls, v):

        class CFConvertSources(BaseModel):

            sink_group_grid_return_temperature: confloat(gt=0,le=95)
            sink_group_grid_supply_temperature: confloat(gt=0,le=95)

            @validator('sink_group_grid_supply_temperature')
            def check_grid_temperatures(cls, v, values, **kwargs):
                if v < values['sink_group_grid_return_temperature']:
                   raise ValueError('Grid supply temperature must be larger than the return temperature.'
                                    ' sink_group_grid_supply_temperature>sink_group_grid_return_temperature')
                return v

        return(CFConvertSources(**v))
