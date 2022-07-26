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



class ReferenceSystemPinch(BaseModel):
    ref_system_eff_equipment: Optional[Union[confloat(gt=0, le=1), None]] = None
    ref_system_fuel_price: Optional[NonNegativeFloat] = None
    ref_system_fuel_type_pinch: Optional[Fuel] = "none"

    @validator('ref_system_fuel_type_pinch', allow_reuse=True, always=True)
    def check_ref_system_fuel_type_is_none(cls, ref_system_fuel_type_pinch, values, **kwargs):

        if ref_system_fuel_type_pinch == "none" and (
                values["ref_system_eff_equipment"] != None or values["ref_system_fuel_price"] != None):
            raise Exception("If Reference System Fuel Type is None -> leave Equipment Efficiency and Fuel Price empty")

        if ref_system_fuel_type_pinch != "none" and values["ref_system_eff_equipment"] == None:
            raise Exception("When introducing Reference System -> fill in the Heating Equipment Efficiency ")

        return ref_system_fuel_type_pinch
