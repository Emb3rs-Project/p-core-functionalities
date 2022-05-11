from pydantic import BaseModel, NonNegativeInt, conlist
from typing import Optional


class GISCorrectSinks(BaseModel):

    sinks: Optional[conlist(NonNegativeInt, min_items=1)] = None
