from pydantic import BaseModel, validator, confloat
from typing import List, Optional
from .Convert_Source_Sink.source_or_sink import SourceOrSink
from .General.location import Location


class MainErrorConvertSources(BaseModel):
    platform: dict
    cf_module: dict
    #gis_module: Optional[dict]

    @validator("platform", "cf_module", always=True)
    def check_if_data_exists(cls, v):

        if v == None:
            raise Exception(
                'Introduce a dictionary with \'platform\', \'cf_module\' and \'gis_module\' (optional)\', and the correspondent necessary data.')

        return v

    @validator('platform', allow_reuse=True)
    def platform_inputs(cls, v):

        class ExistingGridLinkPointData(BaseModel):
            id: int
            location: Location
            levelized_co2_emissions: confloat(ge=0)
            levelized_om_var: confloat(ge=0)
            levelized_om_fix: confloat(ge=0)

        class PlatformConvertSources(BaseModel):
            group_of_sources: List[SourceOrSink]
            existing_grid_data: Optional[ExistingGridLinkPointData] = None

            @validator('group_of_sources', allow_reuse=True)
            def check_if_there_are_sources(cls, v):
                if len(v) < 1:
                    raise ValueError('Introduce at least 1 source to assess a possible District Heating Network.')
                return v

        return (PlatformConvertSources(**v))

    #@validator('gis_module', allow_reuse=True)
    #def gis_module_inputs(cls, v):
#
    #    class GISConvertSources(BaseModel):
    #        sources_losses: Optional[List[GISSourceLosses]]
#
    #    return (GISConvertSources(**v))

    @validator('cf_module', allow_reuse=True)
    def cf_module_inputs(cls, v):

        class CFConvertSources(BaseModel):
            sink_group_grid_return_temperature: confloat(gt=0, le=110)
            sink_group_grid_supply_temperature: confloat(gt=0, le=110)

            @validator('sink_group_grid_supply_temperature', allow_reuse=True)
            def check_grid_temperatures(cls, v, values, **kwargs):
                if v < values['sink_group_grid_return_temperature']:
                    raise ValueError('District Heating Network supply temperature must be larger than the return temperature.')
                return v

        return (CFConvertSources(**v))
