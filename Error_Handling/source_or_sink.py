from pydantic import BaseModel, validator, confloat
from typing import List
from .consumer_type_options import ConsumerTypeOptions
from .stream import Stream
from .location import Location

class SourceOrSink(Location):

    id: int
    consumer_type: ConsumerTypeOptions
    streams: List[Stream]

    @validator('streams')
    def check_if_there_are_streams(cls, v):
        if len(v) < 1:
            raise ValueError('Introduce at least 1 stream for each sink')
        return v

