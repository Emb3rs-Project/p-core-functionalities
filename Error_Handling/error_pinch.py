from pydantic import BaseModel, validator, PositiveFloat, PositiveInt, conlist, NonNegativeInt, StrictStr, \
    NonNegativeFloat,confloat
from typing import Optional, List, Union
from module.Error_Handling.General.location import Location
from .Source_Detail.fuel_type import FuelType
from enum import Enum


def error_convert_pinch(platform_data):
    class StreamType(str, Enum):

        inflow = 'inflow'
        outflow = 'outflow'
        excess_heat = 'excess_heat'
        supply_heat = 'supply_heat'
        hot_stream = "hot_stream"
        cold_stream = "cold_stream"
        startup = "startup"
        maintenance = "maintenance"

    class StreamPinch(BaseModel):

        id: int
        name: str
        object_type: str
        stream_type: StreamType
        supply_temperature: PositiveFloat
        target_temperature: PositiveFloat
        fluid: StrictStr
        flowrate: Union[PositiveFloat, None]
        schedule: conlist(float)
        hourly_generation: conlist(NonNegativeFloat)
        capacity: PositiveFloat

        object_linked_id: Optional[float] = None
        fuel: Optional[FuelType]
        eff_equipment: Optional[confloat(gt=0,le=1)]


        @validator('schedule')
        def check_if_valid_values(cls, v):
            _v = list(filter(lambda num: num < 0, v))
            _v = list(filter(lambda num: num > 1, _v))

            if len(_v) > 0:
                raise ValueError('Values not valid found (only 0 or 1)')
            return v

    class TrueFalse(int, Enum):
        true = 1
        false = 0

    class ObjectType(str, Enum):
        process = "process"
        stream = "stream"
        equipment = "equipment"

    class ProcessorEquipment(BaseModel):
        id: NonNegativeInt
        equipment_id: Optional[NonNegativeInt]
        fuel_type: Optional[FuelType]
        streams: Optional[List[StreamPinch]]
        global_conversion_efficiency: Optional[confloat(gt=0)]
        object_type: ObjectType

        @validator("object_type")
        def validate_if_all_info_in_object(cls, object_type, values, **kwargs):

            if object_type == "process":
                if values['equipment_id'] is None:
                    raise Exception(
                        ' All processes must have an equipment associated (missing Process key:\'equipment_id\').')

            elif object_type == "equipment":
                if values['fuel_type'] is None:
                    raise Exception(
                        ' All equipment must have a fuel type associated (missing Equipment key:\'fuel_type\').')

                if values['global_conversion_efficiency'] is None:
                    raise Exception(
                        ' All equipment must have a conversion efficiency associated (missing Equipment key:\'global_conversion_efficiency\').')

            return object_type

    class ObjectData(BaseModel):
        id: NonNegativeInt
        object_type: ObjectType

    class PlatformPinch(Location):

        all_input_objects: List[ObjectData]
        streams_to_analyse: conlist(int, min_items=1)
        pinch_delta_T_min: Optional[PositiveFloat] = 20
        perform_all_combinations: Optional[TrueFalse] = True
        lifetime: Optional[PositiveInt] = 20
        number_output_options: Optional[PositiveInt] = 3

        @validator("perform_all_combinations")
        def check_perform_all_combinations(cls, v):
            if v == 1:
                return True
            else:
                return False

    # general check
    main_data = PlatformPinch(**platform_data)
    all_objects = []

    # isolated streams check
    for object in platform_data['all_input_objects']:
        if object['object_type'] == "stream":
            new_object = StreamPinch(**object)
        else:
            new_object = ProcessorEquipment(**object)

            new_object.streams = [vars(stream) for stream in new_object.streams]

        all_objects.append(new_object)

    main_data.all_input_objects = all_objects

    return main_data
