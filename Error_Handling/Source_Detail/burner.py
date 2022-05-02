from pydantic import validator, PositiveFloat, confloat, conlist
from typing import Optional
from enum import Enum
from ..General.schedule import Schedule
from .source_detailed_object import SourceDetailedObject
from .fuel_type import FuelType


class BurnerEquipmentSubType(str, Enum):
    direct_burner = "direct_burner"
    indirect_burner = "indirect_burner"


class Burner(SourceDetailedObject, Schedule):
    global_conversion_efficiency: confloat(gt=0, le=1)
    fuel_type: FuelType
    burner_equipment_sub_type: BurnerEquipmentSubType
    burner_excess_heat_supply_temperature: PositiveFloat
    burner_excess_heat_flowrate: PositiveFloat
    supply_capacity: Optional[PositiveFloat]
    processes_id: Optional[conlist(int)]

    @validator("supply_capacity", always=True)
    def provide_supply_capacity_or_processes(cls, v, values, **kwargs):
        if v is None and values['processes_id'] is None:
            raise Exception('Provide equipment supply capacity or the processes associated')

        return v
