from pydantic import validator, PositiveInt
from typing import List, Optional
from .stream import Stream
from .location import Location
from .consumer_type_options import ConsumerTypeOptions


class PlatformConvertORC(Location):

    streams: List[Stream]
    consumer_type: ConsumerTypeOptions
    get_best_number: Optional[PositiveInt]
    orc_years_working: Optional[PositiveInt]

    @validator('streams')
    def check_if_there_are_streams(cls, v):
        if len(v) < 1:
           raise ValueError('Introduce at least 1 stream')
        return v