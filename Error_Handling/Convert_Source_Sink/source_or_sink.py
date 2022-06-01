from pydantic import validator
from typing import List
from ..General.consumer_type_options import ConsumerTypeOptions
from ..General.stream import Stream
from ..General.location import Location


class SourceOrSink(Location):
    id: int
    consumer_type: ConsumerTypeOptions
    streams: List[Stream]

    @validator('streams', allow_reuse=True)
    def check_if_there_are_streams(cls, v):
        if len(v) < 1:
            raise ValueError('Introduce at least 1 stream for each sink')
        return v
