from enum import Enum
from pydantic import BaseModel,validator, PositiveFloat, confloat, conlist, NonNegativeFloat
from typing import Optional,Union


class FuelChoices(str, Enum):
    electricity = "electricity"
    natural_gas = "natural_gas"
    biomass = "biomass"
    fuel_oil = "fuel_oil"
    none = "none"


class FuelType(BaseModel):
    fuel_type: FuelChoices



