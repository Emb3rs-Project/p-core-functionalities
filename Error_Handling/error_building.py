from pydantic import BaseModel, validator, confloat, PositiveFloat, conint, PositiveInt, Required
from typing import Optional, List
from .schedule import Schedule
from.location import Location
from enum import Enum


class BuildingType(str, Enum):

    value_1 = 'office'
    value_2 = 'hotel'
    value_3 = 'residential'


class PlatformBuilding(Schedule, Location):

    number_floor: PositiveFloat
    width_floor: PositiveFloat
    length_floor: PositiveFloat
    height_floor: PositiveFloat
    ratio_wall_N: confloat(ge=0, le=1)
    ratio_wall_S: confloat(ge=0, le=1)
    ratio_wall_E: confloat(ge=0, le=1)
    ratio_wall_W: confloat(ge=0, le=1)
    building_type: BuildingType
    building_orientation: str
    T_heat_on: PositiveFloat = None
    T_cool_on: PositiveFloat = None
    T_off_min: PositiveFloat = None
    T_off_max: PositiveFloat = None

    space_heating_type: Optional[int]
    number_rooms: Optional[PositiveInt]
    number_person_per_floor: Optional[PositiveInt]

    supply_temperature_heat: Optional[PositiveFloat]
    target_temperature_heat: Optional[PositiveFloat]
    supply_temperature_cool: Optional[PositiveFloat]
    target_temperature_cool: Optional[PositiveFloat]
    tau_glass: Optional[confloat(gt=0, le=1)]
    alpha_wall: Optional[confloat(gt=0, le=1)]
    alpha_floor: Optional[confloat(gt=0, le=1)]
    alpha_glass: Optional[confloat(gt=0, le=1)]
    emissivity_wall: Optional[confloat(gt=0, le=1)]
    emissivity_glass: Optional[confloat(gt=0, le=1)]
    u_wall: Optional[confloat(gt=0, le=15)]
    u_roof: Optional[confloat(gt=0, le=15)]
    u_glass: Optional[confloat(gt=0, le=15)]
    u_floor: Optional[confloat(gt=0, le=15)]
    cp_floor: Optional[confloat(gt=5 * 10 ** 4, le=2.5 * 10 ** 5)]
    cp_roof: Optional[confloat(gt=5 * 10 ** 4, le=2.5 * 10 ** 5)]
    cp_wall: Optional[confloat(gt=5 * 10 ** 3, le=9 * 10 ** 4)]
    air_change_hour: Optional[confloat(gt=0, le=60)]
    renewal_air_per_person: Optional[confloat(gt=0, le=0.05)]
    vol_dhw_set: Optional[PositiveFloat]
    Q_gain_per_floor: Optional[PositiveFloat]


    @validator('building_orientation')
    def check_building_orientation(cls, v):
        orientations = ['N', 'S', 'E', 'W']
        if v not in orientations:
            raise ValueError('var:building_orientation value not valid. \n'
                             'Building orientation must be one of the following:', orientations)
        return v


    @validator('T_cool_on')
    def check_occupied_temperatures_set_points(cls, v, values, **kwargs):
        if v != None and values['T_heat_on'] != None:
            if values['T_heat_on'] >= v:
                raise ValueError(
                    'Occupied periods temperature set point to activate heating must be lower than temperature set point to activate cooling. \n T_heat_on < T_cool_on')
        return v


    @validator('T_off_max')
    def check_unoccupied_temperatures_set_points(cls, v, values, **kwargs):
        if v != None and values['T_off_min'] != None:
            if values['T_off_min'] >= v:
                raise ValueError(
                    'Unoccupied periods temperature set point to activate heating must be lower than temperature set point to activate cooling. \n T_heat_on < T_cool_on')
        return v


    @validator('space_heating_type')
    def check_if_valid_value(cls, v):
        valid_values = [0, 1]
        if v not in valid_values:
            raise ValueError('var:space_heating_type value not valid. \n'
                             'Valid options:' + str(valid_values) +
                             '\n Heaters fluid working at  0) 45ºC - 75ºC; 1) 30ºC - 50ºC ')
        return v
