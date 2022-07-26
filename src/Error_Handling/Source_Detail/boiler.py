from pydantic import validator, PositiveFloat, confloat, conlist, NonNegativeFloat
from typing import Optional
from .error_fueltype import FuelType
from ..General.schedule import Schedule
from .source_detailed_object import SourceDetailedObject
from enum import Enum


class OpenClosedCircuit(int, Enum):
    open_circuit = 0
    closed_circuit = 1

class BoilerType(str, Enum):
    steam_boiler = "steam_boiler"
    hot_water_boiler = "hot_water_boiler"

class Boiler(SourceDetailedObject, Schedule,FuelType):

    supply_capacity: PositiveFloat
    open_closed_loop: OpenClosedCircuit
    equipment_supply_temperature: PositiveFloat
    equipment_return_temperature: Optional[PositiveFloat]
    global_conversion_efficiency: Optional[confloat(gt=0, lt=1)]
    boiler_supply_flowrate: Optional[PositiveFloat]
    boiler_equipment_sub_type: BoilerType


    @validator("boiler_supply_flowrate", always=True)
    def provide_boiler_supply_flowrate(cls, boiler_supply_flowrate, values, **kwargs):
       if values['equipment_supply_temperature']>100 and boiler_supply_flowrate == None:
           raise Exception('Provide Boiler Supply Flowrate (condensate) when introducing steam boilers')

       return boiler_supply_flowrate



    @validator('equipment_return_temperature', always=True)
    def check_equipment_return_temperature(cls, equipment_return_temperature, values, **kwargs):

        if values['open_closed_loop'] == 1 and equipment_return_temperature is None:
            raise ValueError("For closed loop Boilers, provide the working fluid return temperature")

        elif values['open_closed_loop'] == 0 and equipment_return_temperature is not None:
            if equipment_return_temperature >= values['equipment_supply_temperature']:
                raise ValueError(
                    "Boiler working fluid return temperature not valid. Return temperature must be lower than supply temperature.")
            else:
                return equipment_return_temperature
        else:
            if equipment_return_temperature >= values['equipment_supply_temperature']:
                raise ValueError(
                    "Boiler working fluid return temperature not valid. Return temperature must be lower than supply temperature.")
            else:
                return equipment_return_temperature
