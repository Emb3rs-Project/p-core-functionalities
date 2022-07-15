from typing import List
from enum import Enum
from .General.simple_industry_stream_data_input import SimpleIndustryStreamDataInput
from pydantic import BaseModel

class TypeofObject(str, Enum):
    source = "source"
    sink = "sink"


class PlatformSimpleUser(BaseModel):
    type_of_object: TypeofObject
    streams: List[SimpleIndustryStreamDataInput]
