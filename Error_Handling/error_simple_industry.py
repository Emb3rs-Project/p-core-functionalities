from pydantic import BaseModel, NonNegativeInt
from typing import List
from enum import Enum
from .General.simple_industry_stream_data_input import SimpleIndustryStreamDataInput

class TypeofObject(str, Enum):
    source = "source"
    sink = "sink"

class PlatformSimpleIndustry(BaseModel):

    type_of_object: TypeofObject
    streams: List[SimpleIndustryStreamDataInput]

