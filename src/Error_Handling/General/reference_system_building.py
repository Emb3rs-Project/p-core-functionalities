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



class ReferenceSystemBuilding(BaseModel):
    ref_system_eff_equipment_heating: Optional[Union[PositiveFloat, None]] = None
    ref_system_fuel_type_heating: Optional[Fuel] = "none"
    ref_system_eff_equipment_cooling: Optional[Union[PositiveFloat, None]] = None
    ref_system_fuel_type_cooling: Optional[Fuel] = "none"



    @validator('ref_system_fuel_type_heating', allow_reuse=True, always=True)
    def check_ref_system_fuel_type_is_none_heating(cls, ref_system_fuel_type, values, **kwargs):


        if ref_system_fuel_type == "none" and values["ref_system_eff_equipment_heating"] != None:
            raise Exception("When introducing Reference System as NONE -> leave reference system fields empty")

        if ref_system_fuel_type != "none" and values["ref_system_eff_equipment_heating"] == None:
            raise Exception("When introducing Reference System -> fill in the Heating Equipment Efficiency ")

        return ref_system_fuel_type

    @validator('ref_system_fuel_type_cooling', allow_reuse=True, always=True)
    def check_ref_system_fuel_type_is_none_cooling(cls, ref_system_fuel_type, values, **kwargs):

        if ref_system_fuel_type == "none" and values["ref_system_eff_equipment_cooling"] != None:
            raise Exception("When introducing Reference System as NONE -> leave reference system fields empty")

        if ref_system_fuel_type != "none" and values["ref_system_eff_equipment_cooling"] == None:
            raise Exception("When introducing Reference System -> fill in the Cooling Equipment Efficiency ")

        return ref_system_fuel_type




