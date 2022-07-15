from pydantic import BaseModel, validator, conlist, PositiveFloat, StrictStr, NonNegativeFloat, confloat
from typing import Optional, Union
from enum import Enum


class ScheduleInfo(int, Enum):
    off = 0
    on = 1


class Fuel(str, Enum):
    natural_gas = "natural_gas"
    electricity = "electricity"
    biomass = "biomass"
    fuel_oil = "fuel_oil"
    none = "none"


class ReferenceSystem(BaseModel):
    ref_system_eff_equipment: Optional[Union[confloat(gt=0, le=1), None]] = None
    ref_system_fuel_type: Optional[Fuel] = "none"

    @validator("ref_system_fuel_type")
    def check_whether_it_is_none(cls, ref_system_fuel_type,values,**kwargs):

        if ref_system_fuel_type == "none" and (values["ref_system_eff_equipment"] != None):
            raise Exception("If Reference System Fuel Type is None -> leave Equipment Efficiency empty")

        if ref_system_fuel_type != "none" and values["ref_system_eff_equipment"] == None:
            raise Exception("When introducing Reference System -> fill in the Equipment Efficiency ")

        return ref_system_fuel_type




