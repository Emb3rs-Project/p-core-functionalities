from pydantic import BaseModel, PositiveInt
from typing import List
from enum import Enum
from .General.stream import Stream

class TypeofObject(str, Enum):
    source = "source"
    sink = "sink"

class PlatformSimpleIndustry(BaseModel):

    object_id: PositiveInt
    type_of_object: TypeofObject
    streams: List[Stream]

