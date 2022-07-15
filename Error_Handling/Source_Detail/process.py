from pydantic import BaseModel, PositiveInt, PositiveFloat, confloat, validator
from typing import List, Optional
from .source_detailed_object import SourceDetailedObject
from ..General.schedule import Schedule
from enum import Enum


class Inflow(BaseModel):
    name: str
    flowrate: Optional[PositiveFloat] = None
    fluid_cp: PositiveFloat
    supply_temperature: PositiveFloat
    fluid: str
    mass: Optional[PositiveFloat] = None

    @validator("mass",allow_reuse=True, always=True)
    def get_flowrate_or_mass(cls, mass, values, **kwargs):

        if (mass == None and values["flowrate"] == None) or (mass != None and values["flowrate"] != None):
            raise Exception('Introduce INFLOW mass flowrate [kg/h] or mass [kg]')

        return mass

class Outflow(BaseModel):
    name: str
    flowrate: Optional[PositiveFloat] = None
    fluid_cp: PositiveFloat
    target_temperature: PositiveFloat
    fluid: str
    mass: Optional[PositiveFloat] = None
    initial_temperature: Optional[PositiveFloat] = None


    @validator("mass", allow_reuse=True, always=True)
    def get_flowrate_or_mass(cls, mass, values, **kwargs):
        if (mass == None and values["flowrate"] == None) or (mass != None and values["flowrate"] != None):
            raise Exception('Introduce OUTFLOW mass flowrate [kg/h] or mass [kg]')

        return mass

class Maintenance(BaseModel):
    name: str
    maintenance_capacity: PositiveFloat

class ScheduleType(int, Enum):
    continuous = 0
    batch = 1


class Process(SourceDetailedObject, Schedule):
    equipment_id: PositiveInt
    operation_temperature: PositiveFloat
    schedule_type: ScheduleType
    cycle_time_percentage: confloat(gt=0, le=1)
    maintenance_data: Optional[List[Maintenance]] = []
    inflow_data: Optional[List[Inflow]] = []
    outflow_data: Optional[List[Outflow]] = []
