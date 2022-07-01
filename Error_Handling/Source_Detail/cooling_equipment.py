from pydantic import validator, PositiveFloat, confloat, conlist
from ..General.schedule import Schedule
from typing import Optional
from .source_detailed_object import SourceDetailedObject
from enum import Enum


class CoolingEquipmentSubType(str, Enum):
    compression_chiller = "compression_chiller"
    co2_chiller = "co2_chiller"
    cooling_tower = "cooling_tower"


class CoolingEquipment(SourceDetailedObject, Schedule):
    cooling_equipment_sub_type: CoolingEquipmentSubType
    supply_capacity: PositiveFloat
    global_conversion_efficiency: Optional[confloat(gt=2, le=20)]

