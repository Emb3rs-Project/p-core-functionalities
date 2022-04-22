from pydantic import BaseModel, validator
from typing import List
from .source_or_sink import SourceOrSink

class PlatformConvertSinks(BaseModel):

    group_of_sinks: List[SourceOrSink]

    @validator('group_of_sinks')
    def check_if_there_are_sinks(cls, v):
        if len(v) < 1:
           raise ValueError('Introduce at least 1 sink')
        return v
