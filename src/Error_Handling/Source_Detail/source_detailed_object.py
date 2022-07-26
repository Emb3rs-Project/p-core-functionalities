from pydantic import BaseModel, PositiveInt
from enum import Enum


class ObjectType(str, Enum):
    process = "process"
    boiler = "boiler"
    chp = "chp"
    burner = "burner"
    cooling_equipment = "cooling_equipment"
    stream = "stream"


class SourceDetailedObject(BaseModel):
    object_type: ObjectType
    id: PositiveInt
