from pydantic import validator, PositiveFloat, confloat, conlist, NonNegativeFloat
from typing import Optional
from enum import Enum
from ..General.schedule import Schedule
from .source_detailed_object import SourceDetailedObject
from .error_fueltype import FuelType


class BurnerEquipmentSubType(str, Enum):
    direct_burner = "direct_burner"
    indirect_burner = "indirect_burner"


class Burner(SourceDetailedObject, Schedule,FuelType):

    global_conversion_efficiency: confloat(gt=0, le=1)
    burner_equipment_sub_type: BurnerEquipmentSubType
    burner_excess_heat_supply_temperature: PositiveFloat
    burner_excess_heat_flowrate: PositiveFloat
    supply_capacity: PositiveFloat


