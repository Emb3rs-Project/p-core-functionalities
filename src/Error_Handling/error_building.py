from pydantic import validator, confloat, PositiveFloat, PositiveInt, StrictStr
from typing import Optional

from .General.reference_system_building import ReferenceSystemBuilding
from .General.schedule import Schedule
from .General.location import Location
from enum import Enum
import ast
from .General.error_building_and_greenhouse_adjust_capacity import BuildingandGreenhouseAdjustCapacity
from ..KB_General.building_properties import BuildingProperties
from ..General.Auxiliary_General.get_country import get_country
from .General.building_orientation import BuildingOrientation

class ScheduleInfo(int, Enum):
    off = 0
    on = 1

def error_building(platform_data, kb):
    building_properties = BuildingProperties(kb)

    class BuildingType(str, Enum):
        office = 'office'
        hotel = 'hotel'
        residential = 'residential'

    class SpaceHeatingType(int, Enum):
        conventional = 1
        low_temperature = 2
        user_input = 3

    class PlatformBuildingInitial(Location):
        width_floor: PositiveFloat
        length_floor: PositiveFloat
        space_heating_type: SpaceHeatingType
        number_rooms: Optional[PositiveInt]
        number_person_per_floor: Optional[PositiveInt]
        supply_temperature_heat: Optional[PositiveFloat]
        target_temperature_heat: Optional[PositiveFloat]
        building_type: BuildingType

        @validator('building_type', allow_reuse=True)
        def check_hotel(cls, v, values, **kwargs):
            if v == 'hotel' and values['number_rooms'] == None:
                raise Exception(
                    'If building type is hotel, introduce number of rooms per floor in the ADVANCED PROPERTIES section.')
            elif v == 'residential' and values['number_person_per_floor'] == None:
                raise Exception(
                    'If building type is residential, introduce number of persons per floor in the ADVANCED PROPERTIES section.')

            return v

    ########################################################################################
    ########################################################################################

    initial_data = PlatformBuildingInitial(**platform_data)

    # give default values
    latitude, longitude = initial_data.location
    building_type = initial_data.building_type
    area_floor = initial_data.width_floor * initial_data.length_floor
    country = get_country(latitude, longitude)
    space_heating_type = int(initial_data.space_heating_type)

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

    class PlatformBuilding(Location, ReferenceSystemBuilding, BuildingandGreenhouseAdjustCapacity):

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

        monday_daily_periods: Optional[StrictStr]
        tuesday_daily_periods: Optional[StrictStr]
        wednesday_daily_periods: Optional[StrictStr]
        thursday_daily_periods: Optional[StrictStr]
        friday_daily_periods: Optional[StrictStr]
        saturday_daily_periods: Optional[StrictStr]
        sunday_daily_periods: Optional[StrictStr]

        daily_periods: Optional[str]
        shutdown_periods: Optional[str]
        saturday_on: Optional[ScheduleInfo]
        sunday_on: Optional[ScheduleInfo]

        @validator('T_cool_on', allow_reuse=True)
        def check_occupied_temperatures_set_points(cls, T_cool_on, values, **kwargs):
            if values['T_heat_on'] >= T_cool_on:
                raise ValueError(
                    'Occupied periods Heating Setpoint temperature must be lower than the Cooling Setpoint temperature.')
            return T_cool_on

        @validator('T_off_max', allow_reuse=True)
        def check_unoccupied_temperatures_set_points(cls, supply_temperature_heat, values, **kwargs):
            if values['T_off_min'] >= supply_temperature_heat:
                raise ValueError(
                    'Unoccupied periods Heating Setback temperature must be lower than the Cooling Setback temperature.')
            return supply_temperature_heat

        @validator('supply_temperature_heat', allow_reuse=True)
        def check_supply_and_target_temperature_heat(cls, supply_temperature_heat, values, **kwargs):

            if values['target_temperature_heat'] <= supply_temperature_heat:
                raise ValueError(
                    'Heating System Supply Temperature must be larger than Heating System Return Temperature.')
            return supply_temperature_heat

        @validator("daily_periods",
                   "monday_daily_periods",
                   "tuesday_daily_periods",
                   "wednesday_daily_periods",
                   "thursday_daily_periods",
                   "friday_daily_periods",
                   "saturday_daily_periods",
                   "sunday_daily_periods",allow_reuse=True )
        def check_structure_daily_periods(cls, daily_periods):
            daily_periods = ast.literal_eval(daily_periods)
            if daily_periods != []:
                if isinstance(daily_periods, list) is True:
                    for period in daily_periods:
                        if len(period) != 2:
                            raise ValueError(
                                'Only a start and ending hour must be given in each daily period. Example: [[9,12],[14,19]]')
                        else:
                            period_a, period_b = period
                            if period_b <= period_a:
                                raise ValueError(
                                    'Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]')
                else:
                    raise TypeError('Provide a list for daily periods.')
            else:
                raise TypeError('Provide daily periods in the correct format. Example: [[11,20]] or [[9,12],[14,19]]')

            return daily_periods

        @validator('shutdown_periods',allow_reuse=True )
        def check_structure_shutdown_periods(cls, shutdown_periods):

            shutdown_periods = ast.literal_eval(shutdown_periods)
            if shutdown_periods != []:
                if isinstance(shutdown_periods, list) is True:
                    for period in shutdown_periods:
                        if len(period) != 2:
                            raise ValueError(
                                'Only a start and ending day must be given in each shutdown period. Example: [[220,250]]')
                        else:
                            period_a, period_b = period
                            if period_b <= period_a:
                                raise ValueError(
                                    'Second value of the shutdown period must be larger than the first. Example: [[220,250]]')
                else:
                    raise TypeError(
                        'Provide a list for shutdown periods.')

            return shutdown_periods

    return PlatformBuilding(**platform_data)
