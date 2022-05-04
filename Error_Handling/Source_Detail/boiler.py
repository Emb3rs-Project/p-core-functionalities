from pydantic import validator, PositiveFloat, confloat, conlist
from typing import Optional
from .fuel_type import FuelType
from ..General.schedule import Schedule
from .source_detailed_object import SourceDetailedObject
from enum import Enum


class OpenClosedCircuit(int, Enum):
    open_circuit = 0
    closed_circuit = 1


class Boiler(SourceDetailedObject, Schedule):
    fuel_type: FuelType
    open_closed_loop: OpenClosedCircuit
    equipment_supply_temperature: PositiveFloat
    equipment_return_temperature: Optional[PositiveFloat]
    processes_id: Optional[conlist(int)]
    supply_capacity: Optional[PositiveFloat]
    global_conversion_efficiency: Optional[confloat(gt=0, lt=1)]

    @validator("supply_capacity", always=True)
    def provide_supply_capacity_or_processes(cls, v, values, **kwargs):
        if v is None and values['processes_id'] is None:
            raise Exception('Provide equipment supply capacity or the processes associated')

        return v

    @validator('equipment_return_temperature', always=True)
    def check_equipment_return_temperature(cls, equipment_return_temperature, values, **kwargs):

        if values['open_closed_loop'] == 1 and equipment_return_temperature is None:
            raise ValueError("For closed loop equipment, provide the working fluid return temperature")

        elif values['open_closed_loop'] == 0 and equipment_return_temperature is not None:
            if equipment_return_temperature >= values['equipment_supply_temperature']:
                raise ValueError(
                    "Equipment working fluid return temperature not valid. Return temperature must be lower than supply temperature.")
            else:
                return equipment_return_temperature
        else:
            if equipment_return_temperature >= values['equipment_supply_temperature']:
                raise ValueError(
                    "Equipment working fluid return temperature not valid. Return temperature must be lower than supply temperature.")
            else:
                return equipment_return_temperature