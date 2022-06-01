from pydantic import BaseModel
from typing import List
from .General.simple_industry_stream_data_input import SimpleIndustryStreamDataInput


class PlatformIsolatedStream(BaseModel):
    streams: List[SimpleIndustryStreamDataInput]
