from pydantic import validator, PositiveFloat, confloat
from typing import Optional
from .error_fueltype import FuelType
from .source_detailed_object import SourceDetailedObject
from ..General.schedule import Schedule


class Chp(SourceDetailedObject, Schedule, FuelType):
    global_conversion_efficiency: confloat(gt=0, lt=1)
    supply_capacity: PositiveFloat
    electrical_generation: Optional[PositiveFloat]
    thermal_conversion_efficiency: Optional[confloat(gt=0, lt=1)]
    electrical_conversion_efficiency: Optional[confloat(gt=0, lt=1)]

    @validator("thermal_conversion_efficiency", pre=True)
    def provide_thermal_or_electrical_efficiency(cls, v, values, **kwargs):

        if v is None and values['electrical_conversion_efficiency'] is None:
            raise Exception('Provide CHP thermal or electrical conversion efficiency.')

        return v

