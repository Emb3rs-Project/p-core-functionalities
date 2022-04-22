from pydantic import validator, confloat, PositiveFloat
from typing import Optional
from .schedule import Schedule
from .location import Location


class PlatformGreenhouse(Schedule,Location):

    width: PositiveFloat
    length: PositiveFloat
    height: PositiveFloat
    greenhouse_orientation: str
    lights_on: int
    T_heat_on: PositiveFloat
    T_cool_on: PositiveFloat
    thermal_blanket: int
    greenhouse_efficiency: int
    sunday_on: int = 1
    saturday_on: int = 1

    f_c: Optional[confloat(gt=0, le=30*10**(-4))] = None
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


    @validator('greenhouse_orientation')
    def check_greenhouse_orientation(cls, v):
        orientations = ['N', 'S', 'E', 'W']
        if v not in orientations:
           raise ValueError('Greenhouse orientation must be one of the following:', orientations)
        return v

    @validator('greenhouse_efficiency')
    def check_greenhouse_efficiency(cls, v, values, **kwargs):

        if v == None and values['f_c'] == None:
            raise ValueError('Insert greenhouse efficiency or Fc')

        else:

            if v != None:
                efficiency = [1,2,3,4]

                if v not in efficiency:
                   raise ValueError('Greenhouse efficiency must be one of the following:', efficiency)
                else:
                    return v

            else:

                return v

    @validator('f_c')
    def check_f_c(cls, v, values, **kwargs):
        if v == None and values['greenhouse_efficiency'] == None:
            raise ValueError('Insert greenhouse efficiency or Fc')

        else:
            if v == None:
                if values['greenhouse_efficiency'] == 1:
                    v = 2.5 * 10 ** (-4)  # factor to estimate building infiltrations
                elif values['greenhouse_efficiency'] == 2:
                    v = 5 * 10 ** (-4)
                else:
                    v = 15 * 10 ** (-4)

                return v

            else:
                return v



    @validator('lights_on','thermal_blanket')
    def check_if_exist(cls, v):
        valid_values = [0, 1]
        if v not in valid_values:
           raise ValueError('Not valid values. 0-no; 1-yes')
        return v

    @validator('T_cool_on')
    def check_temperatures_set_points(cls, v, values, **kwargs):
        if values['T_heat_on'] >= v:
           raise ValueError('Temperature set point to activate heating must be lower than temperature set point to activate cooling. T_heat_on < T_cool_on')
        return v

    @validator('supply_temperature_heat')
    def check_heaters_temperatures(cls, v, values, **kwargs):
        if values['target_temperature_heat'] >= v:
           raise ValueError('var:supply_temperature_heat < target_temperature_heat. The supply_temperature_heat, is th heaters supply fluid temperature to the DHN heat exchanger.')
        return v
