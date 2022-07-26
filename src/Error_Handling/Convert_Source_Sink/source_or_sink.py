from pydantic import validator
from typing import List
from ..General.stream import Stream
from ..General.location import Location
from ..General.fueldata import FuelData

class SourceOrSink(Location):
    id: int
    streams: List[Stream]
    fuels_data: FuelData


    @validator('streams', allow_reuse=True)
    def check_if_there_are_streams(cls, v):
        if len(v) < 1:
            raise ValueError('Introduce at least 1 stream for each Sink')
        return v
