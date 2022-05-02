from enum import Enum


class FuelType(str, Enum):
    electricity = "electricity"
    natural_gas = "natural_gas"
    biomass = "biomass"
    fuel_oil = "fuel_oil"
