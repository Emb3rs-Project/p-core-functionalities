from pydantic import validator, confloat, PositiveFloat, PositiveInt
from typing import Optional
from .General.schedule import Schedule
from .General.location import Location
from enum import Enum
from ..KB_General.building_properties import BuildingProperties
from ..General.Auxiliary_General.get_country import get_country
from .General.building_orientation import BuildingOrientation


def error_building(platform_data,kb):

    building_properties = BuildingProperties(kb)

    class BuildingType(str, Enum):
        office = 'office'
        hotel = 'hotel'
        residential = 'residential'

    class SpaceHeatingType(str, Enum):
        conventional = "1"
        low_temperature = "2"
        user_input = "3"

    class PlatformBuildingInitial(Location):
        building_type: BuildingType
        width_floor: PositiveFloat
        length_floor: PositiveFloat
        space_heating_type: SpaceHeatingType
        number_rooms: Optional[PositiveInt]
        number_person_per_floor: Optional[PositiveInt]
        supply_temperature_heat: Optional[PositiveFloat]
        target_temperature_heat: Optional[PositiveFloat]


        @validator('building_type',allow_reuse=True)
        def check_hotel(cls, v, values, **kwargs):
            if v == 'hotel' and values['number_rooms'] == None:
                raise Exception('If building type is hotel, introduce number of rooms per floor in the Advanced Parameters section.')
            elif v == 'residential' and values['number_person_per_floor'] == None:
                raise Exception('If building type is residential, introduce number of persons per floor in the Advanced Parameters section.')

            return v


    ########################################################################################
    ########################################################################################

    initial_data = PlatformBuildingInitial(**platform_data)

    latitude, longitude = initial_data.location
    building_type = initial_data.building_type
    area_floor = initial_data.width_floor * initial_data.length_floor
    country = get_country(latitude, longitude)
    space_heating_type = initial_data.space_heating_type

    val_u_wall, val_u_roof, val_u_glass, val_u_floor, val_tau_glass, val_alpha_wall, val_alpha_floor, val_alpha_glass, val_cp_wall, val_cp_floor, val_cp_roof, val_air_change_hour, val_emissivity_wall, val_emissivity_glass = building_properties.get_values(
            country, building_type)

    val_number_rooms = 0

    if building_type == 'residential':
        val_number_person_per_floor = initial_data.number_person_per_floor
        val_Q_gain_per_floor = 4 * area_floor  # occupancy and appliances heat gains [W]
        val_vol_dhw_set = 0.03 * val_number_person_per_floor  # daily dwelling DHW consumption per floor [m3]
        val_renewal_air_per_person = 0  # renewal fresh air [m3/s]
    elif building_type == 'hotel':
        val_number_rooms = initial_data.number_rooms
        val_number_person_per_floor = 2 * val_number_rooms  # number of rooms per floor
        val_vol_dhw_set = 0.03 * val_number_person_per_floor  # daily dwelling DHW consumption [m3]
        val_Q_gain_per_floor = 4 * area_floor  # occupancy and appliances heat gains [W]
        val_renewal_air_per_person = 0  # renewal fresh air [m3/s]
    else:
        val_number_person_per_floor = round(area_floor / 9)  # number of occupants per floor (9m2 per occupant)
        val_vol_dhw_set = 0.003 * val_number_person_per_floor  # daily dwelling DHW consumption [m3]
        val_Q_gain_per_floor = val_number_person_per_floor * 108 + 18 * area_floor  # occupancy and appliances heat gains [W]
        val_renewal_air_per_person = 10 * 10 ** (-3)  # [m3/s] per person

    if space_heating_type == 1:
        platform_data['target_temperature_heat'] = 75
        platform_data['supply_temperature_heat'] = 45
    elif space_heating_type == 2:
        platform_data['target_temperature_heat'] = 50
        platform_data['supply_temperature_heat'] = 30
    else:
        platform_data['target_temperature_heat'] = initial_data.target_temperature_heat
        platform_data['supply_temperature_heat'] = initial_data.supply_temperature_heat


    ########################################################################################
    ########################################################################################

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
        building_orientation: BuildingOrientation
        T_heat_on: Optional[PositiveFloat] = -1000
        T_cool_on: Optional[PositiveFloat] = 1000
        T_off_min: Optional[PositiveFloat] = -1000
        T_off_max: Optional[PositiveFloat] = 1000
        space_heating_type: SpaceHeatingType
        number_rooms: Optional[PositiveInt] = val_number_rooms
        number_person_per_floor: Optional[PositiveInt] = val_number_person_per_floor
        target_temperature_heat: PositiveFloat
        supply_temperature_heat: PositiveFloat
        supply_temperature_cool: Optional[PositiveFloat] = 12
        target_temperature_cool: Optional[PositiveFloat] = 7
        tau_glass: Optional[confloat(gt=0, le=1)] = val_tau_glass
        alpha_wall: Optional[confloat(gt=0, le=1)] = val_alpha_wall
        alpha_floor: Optional[confloat(gt=0, le=1)] = val_alpha_floor
        alpha_glass: Optional[confloat(gt=0, le=1)] = val_alpha_glass
        emissivity_wall: Optional[confloat(gt=0, le=1)] = val_emissivity_wall
        emissivity_glass: Optional[confloat(gt=0, le=1)] = val_emissivity_glass
        u_wall: Optional[confloat(gt=0, le=15)] = val_u_wall
        u_roof: Optional[confloat(gt=0, le=15)] = val_u_roof
        u_glass: Optional[confloat(gt=0, le=15)] = val_u_glass
        u_floor: Optional[confloat(gt=0, le=15)] = val_u_floor
        cp_floor: Optional[confloat(gt=5 * 10 ** 4, le=2.5 * 10 ** 5)] = val_cp_floor
        cp_roof: Optional[confloat(gt=5 * 10 ** 4, le=2.5 * 10 ** 5)] = val_cp_roof
        cp_wall: Optional[confloat(gt=5 * 10 ** 3, le=9 * 10 ** 4)] = val_cp_wall
        air_change_hour: Optional[confloat(gt=0, le=60)] = val_air_change_hour
        renewal_air_per_person: Optional[confloat(gt=0, le=0.05)] = val_renewal_air_per_person
        vol_dhw_set: Optional[PositiveFloat] = val_vol_dhw_set
        Q_gain_per_floor: Optional[PositiveFloat] = val_Q_gain_per_floor


        @validator('T_cool_on')
        def check_occupied_temperatures_set_points(cls, v, values, **kwargs):
            if values['T_heat_on'] >= v:
                raise ValueError(
                        'Occupied periods temperature set point to activate heating must be lower than temperature set point to activate cooling. \n T_heat_on < T_cool_on')
            return v


        @validator('T_off_max')
        def check_unoccupied_temperatures_set_points(cls, v, values, **kwargs):
            if values['T_off_min'] >= v:
                raise ValueError(
                        'Unoccupied periods temperature set point to activate heating must be lower than temperature set point to activate cooling. \n T_heat_on < T_cool_on')
            return v


        @validator('supply_temperature_heat')
        def check_supply_and_target_temperature_heat(cls, v, values, **kwargs):


            if values['target_temperature_heat'] <= v:
                raise ValueError(
                    'Heaters target temperature must be larger than supply.')
            return v


    return PlatformBuilding(**platform_data)
