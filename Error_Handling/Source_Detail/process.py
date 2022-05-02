from pydantic import BaseModel, PositiveInt, PositiveFloat, confloat
from typing import List, Optional
from .source_detailed_object import SourceDetailedObject
from ..General.schedule import Schedule
from enum import Enum

class Inflow(BaseModel):
    flowrate: PositiveFloat
    fluid_cp: PositiveFloat
    supply_temperature: PositiveFloat
    fluid: str


class Outflow(BaseModel):
    flowrate: PositiveFloat
    fluid_cp: PositiveFloat
    target_temperature: PositiveFloat
    fluid: str


class Maintenance(BaseModel):
    maintenance_capacity: PositiveFloat


class Startup(BaseModel):
    mass: PositiveFloat
    fluid_cp: PositiveFloat
    supply_temperature: PositiveFloat
    fluid: str

class ScheduleType(int,Enum):
    continous = 0
    batch = 1


class Process(SourceDetailedObject, Schedule):
    equipment_id: PositiveInt
    operation_temperature: PositiveFloat
    schedule_type: ScheduleType
    cycle_time_percentage: confloat(gt=0, lt=1)
    startup_data: Optional[List[Startup]]
    maintenance_data: Optional[List[Maintenance]]
    inflow_data: Optional[List[Inflow]]
    outflow_data: Optional[List[Outflow]]

