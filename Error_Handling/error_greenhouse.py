from enum import Enum
from typing import Optional

from pydantic import validator, confloat, PositiveFloat, conint, PositiveInt

from .General.building_orientation import BuildingOrientation
from .General.location import Location
from .General.schedule import Schedule


class GreenhouseEfficiency(int, Enum):
    tight_cover = 1
    medium_sealing = 2
    loose_cover = 3
    user_inputs_fc = 4


class ArtificalLights_and_ThermalBlanket(int, Enum):
    has = 1
    does_not_have = 0


class PlatformGreenhouse(Schedule, Location):
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
    f_c: Optional[confloat(gt=0, le=30 * 10 ** (-4))] = None
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

    @validator('f_c',always=True)
    def check_f_c(cls, f_c, values, **kwargs):

        if values['greenhouse_efficiency'] == 1:
            f_c = 2.5 * 10 ** (-4)  # factor to estimate greenhouse infiltrations
        elif values['greenhouse_efficiency'] == 2:
            f_c = 5 * 10 ** (-4)
        elif values['greenhouse_efficiency'] == 3:
            f_c = 15 * 10 ** (-4)
        else:
            if f_c == None:
                raise ValueError(
                    'For greenhouse_efficiency=\'Fc Specifiy\', the user needs to provide a value for Fc in the Advance Parameters.')

        return f_c

    @validator('T_cool_on')
    def check_temperatures_set_points(cls, v, values, **kwargs):
        if values['T_heat_on'] >= v:
            raise ValueError(
                'Temperature set point to activate heating must be lower than temperature set point to activate cooling. T_heat_on < T_cool_on')
        return v

    @validator('supply_temperature_heat')
    def check_heaters_temperatures(cls, v, values, **kwargs):
        if values['target_temperature_heat'] >= v:
            raise ValueError(
                'The \'Heaters low temperature\' (which is the supplied heater\'s fluid temperature to the DHN heat exchanger) must be lower than the \'Heaters high temperature\' (which is the target heater\'s fluid temperature  returning from the to the DHN heat exchanger). supply_temperature_heat < target_temperature_heat.')
        return v

    @validator('artificial_lights_system')
    def check_artificial_lights_system(cls, v, values, **kwargs):
        if v == 1 and values['hours_lights_needed'] is None:
            raise ValueError(
                'When introducing existing artificial lighting system, input daily light hours needed.')
        return v
