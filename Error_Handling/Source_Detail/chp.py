from pydantic import validator, PositiveFloat, confloat, conlist
from typing import Optional
from .fuel_type import FuelType
from .source_detailed_object import SourceDetailedObject
from ..General.schedule import Schedule


class Chp(SourceDetailedObject, Schedule):
    fuel_type: FuelType
    global_conversion_efficiency: confloat(gt=0, lt=1)
    supply_capacity: PositiveFloat
    electrical_generation: Optional[PositiveFloat]
    #processes_id: None
    thermal_conversion_efficiency: Optional[confloat(gt=0, lt=1)]
    electrical_conversion_efficiency: Optional[confloat(gt=0, lt=1)]

    @validator("thermal_conversion_efficiency", pre=True)
    def provide_thermal_or_electrical_efficiency(cls, v, values, **kwargs):

        if v is None and values['electrical_conversion_efficiency'] is None:
            raise Exception('Provide equipment thermal or electrical conversion efficiency.')

        return v

    #@validator("supply_capacity", always=True)
    #def provide_supply_or_electrical_capacity_or_processes(cls, v, values, **kwargs):
    #
    #    if v is None and values['processes_id'] is None and values['electrical_generation'] is None:
    #        raise Exception('Provide equipment thermal capacity, electrical capacity or the processes associated')
    #
    #    return v
    #