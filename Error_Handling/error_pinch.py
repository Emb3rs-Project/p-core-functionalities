from pydantic import BaseModel, validator, PositiveFloat, PositiveInt, conlist
from typing import List, Optional
from .location import Location
from .stream import Stream


from enum import Enum


class Process(BaseModel):


class Equipment(BaseModel):


class ObjectType(str, Enum):

    value_1 = 'stream'
    value_2 = 'process'
    value_3 = 'equipment'


class PinchObject(BaseModel):

    object_type: ObjectType


class PlatformPinch(Location):

    all_input_objects: conlist(dict,min_items=1)
    perform_all_combinations: bool

    pinch_delta_T_min: Optional[PositiveFloat]
    lifetime: Optional[PositiveInt]
    number_output_options:  Optional[PositiveInt]

    @validator('all_input_objects')
    def check_object_type(cls, v):



    @validator('all_input_objects')
    def check_all_input_objects(cls, v):
        streams = []

        for object in v:
            if object['object_type'] == 'process':  # from processes get streams
                Process(**v)
                for stream in object['streams']:
                    if stream['stream_type'] == 'inflow' or stream['stream_type'] == 'outflow':
                        streams.append(stream)
            elif object['object_type'] == 'stream':  # isolated streams
                Stream(**v)
                streams.append(object)

        # if empty, it means analyse equipment internal heat recovery
        if streams == []:
            object = v[0]
            if object['object_type'] == 'equipment':
                Equipment(**v)
                for stream in object['streams']:
                    if stream['stream_type'] == 'excess_heat' or stream['stream_type'] == 'inflow':
                        streams.append(stream)

        if streams == []:
            raise  ('There are no streams to analyze')







