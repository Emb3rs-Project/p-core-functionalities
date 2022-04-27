from pydantic import validator, confloat, PositiveFloat, conint, PositiveInt, BaseModel, EnumError
from typing import Optional
from .schedule import Schedule
from .location import Location
from .building_orientation import BuildingOrientation


def error_greenhouse(platform_data):

    class PlatformInitialGreenhouse(BaseModel):
        greenhouse_efficiency: int

        @validator("greenhouse_efficiency", pre=True)
        def _greenhouse_efficiency(cls, v):
            options = [1,2,3,4]

            if v not in options:
                raise ValueError("Must be an integer corresponding to one of the following options:"
                                 "\n 1) Tight Cover"
                                 "\n 2) Medium sealing"
                                 "\n 3) Loose Cover"
                                 "\n 4) Fc specify \n"
                                 )
            else:
                return v


    inital_data = PlatformInitialGreenhouse(**platform_data)

    if inital_data.greenhouse_efficiency == 1:
        val_f_c = 2.5 * 10 ** (-4)  # factor to estimate building infiltrations
    elif inital_data.greenhouse_efficiency == 2:
        val_f_c = 5 * 10 ** (-4)
    elif inital_data.greenhouse_efficiency == 3:
        val_f_c = 15 * 10 ** (-4)
    else:
        val_f_c = None

    class PlatformGreenhouse(Schedule, Location):

        # Optional
        f_c: Optional[confloat(gt=0, le=30 * 10 ** (-4))] = val_f_c
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
        hours_lights_needed: Optional[conint(gt=0, le=24)] = None

        # Mandatory
        width: PositiveFloat
        length: PositiveFloat
        height: PositiveFloat
        greenhouse_orientation: BuildingOrientation
        lights_on: int
        T_heat_on: PositiveFloat
        T_cool_on: PositiveFloat
        thermal_blanket: int
        greenhouse_efficiency: PositiveInt
        sunday_on: int = 1
        saturday_on: int = 1


        @validator('lights_on', 'thermal_blanket', pre=True)
        def check_if_exist(cls, v):
            valid_values = [0, 1]
            if v not in valid_values:
                raise ValueError( "Must be an integer corresponding to one of the following options:"
                                     '\n 0) No/Does not have'
                                     '\n 1) Yes/Has \n')
            else:
                return v

        @validator('greenhouse_efficiency')
        def check_greenhouse_efficiency(cls, v, values, **kwargs):

            if v == None and values['f_c'] == None:
                raise ValueError('Insert greenhouse efficiency or Fc')

            elif v == 4 and values['f_c'] == None:
                raise ValueError('For greenhouse_efficiency=\'Fc Specifiy\', the user needs to provide a value for Fc in the Advance Parameters.')
            else:
                return v

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

    return PlatformGreenhouse(**platform_data)