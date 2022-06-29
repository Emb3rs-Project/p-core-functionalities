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
    #processes_id: None
    supply_capacity: PositiveFloat
    global_conversion_efficiency: Optional[confloat(gt=2, le=20)]

   # @validator("supply_capacity", always=True)
   # def provide_supply_capacity_or_processes(cls, v, values, **kwargs):
   #     if v is None and values['processes_id'] is None:
   #         raise Exception('Provide equipment supply capacity or the processes associated')
    #
   #     return v
    #