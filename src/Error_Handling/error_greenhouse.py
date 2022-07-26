from enum import Enum
from typing import Optional
from pydantic import validator, confloat, PositiveFloat, conint, PositiveInt
from .General.building_orientation import BuildingOrientation
from .General.location import Location
from .General.reference_system import ReferenceSystem
from .General.schedule import Schedule
from .General.error_building_and_greenhouse_adjust_capacity import BuildingandGreenhouseAdjustCapacity


class GreenhouseEfficiency(int, Enum):
    tight_cover = 1
    medium_sealing = 2
    loose_cover = 3


class ArtificalLights_and_ThermalBlanket(int, Enum):
    has = 1
    does_not_have = 0


class PlatformGreenhouse(Schedule, Location, ReferenceSystem, BuildingandGreenhouseAdjustCapacity):
    # Mandatory
    hours_lights_needed: Optional[conint(gt=0, le=24)] = None
    greenhouse_efficiency: GreenhouseEfficiency
    width: PositiveFloat
    length: PositiveFloat
    height: PositiveFloat
    greenhouse_orientation: BuildingOrientation
    artificial_lights_system: ArtificalLights_and_ThermalBlanket
    T_heat_on: PositiveFloat
    T_cool_on: PositiveFloat = 35
    thermal_blanket: ArtificalLights_and_ThermalBlanket
    greenhouse_efficiency: PositiveInt
    sunday_on: int = 1
    saturday_on: int = 1

    # Optional
    f_c: Optional[float] = None
    supply_temperature_heat: Optional[float] = 30
    target_temperature_heat: Optional[float] = 50
    leaf_area_index: Optional[confloat(gt=0, le=20)] = 1
    rh_air: Optional[confloat(gt=0, le=1)] = 80
    u_cover: Optional[confloat(gt=0, le=9)] = 6
    indoor_air_speed: Optional[confloat(gt=0, le=8)] = 0.1
    leaf_length: Optional[confloat(gt=0, le=1)] = 0.027
    tau_cover_long_wave_radiation: Optional[confloat(gt=0, le=1)] = 0.3
    emissivity_cover_long_wave_radiation: Optional[confloat(gt=0, le=1)] = 0.2
    tau_cover_solar_radiation: Optional[confloat(gt=0, le=1)] = 0.9
    power_lights: Optional[PositiveFloat] = 20

    @validator('f_c', always=True)
    def check_f_c(cls, f_c, values, **kwargs):

        if values['greenhouse_efficiency'] == 1:
            f_c = 2.5 * 10 ** (-4)  # factor to estimate greenhouse infiltrations
        elif values['greenhouse_efficiency'] == 2:
            f_c = 5 * 10 ** (-4)
        elif values['greenhouse_efficiency'] == 3:
            f_c = 15 * 10 ** (-4)

        return f_c

    @validator('T_cool_on')
    def check_temperatures_set_points(cls, T_cool_on, values, **kwargs):
        if values['T_heat_on'] >= T_cool_on:
            raise ValueError(
                'Heating Temperature Setpoint must be lower than Cooling Setpoint Temperature')
        return T_cool_on

    @validator('supply_temperature_heat')
    def check_heaters_temperatures(cls, supply_temperature_heat, values, **kwargs):
        if values['target_temperature_heat'] >= supply_temperature_heat:
            raise ValueError(
                'Heating System Supply Temperature must be larger than Heating System Return Temperature (Advanced Parameters).')
        return supply_temperature_heat

    @validator('artificial_lights_system')
    def check_artificial_lights_system(cls, artificial_lights_system, values, **kwargs):
        if artificial_lights_system == 1 and values['hours_lights_needed'] is None:
            raise ValueError(
                'When introducing existing artificial lighting system, input daily light hours needed (Advanced Parameters).')
        return artificial_lights_system
