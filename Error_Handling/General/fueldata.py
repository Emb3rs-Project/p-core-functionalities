from pydantic import BaseModel, NonNegativeFloat

class Data(BaseModel):
    price: NonNegativeFloat
    co2_emissions: NonNegativeFloat

class FuelData(BaseModel):
    natural_gas: Data
    biomass: Data
    electricity: Data
    fuel_oil: Data





