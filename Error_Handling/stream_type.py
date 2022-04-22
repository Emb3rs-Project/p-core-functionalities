from enum import Enum


class StreamType(str, Enum):
    value_1 = 'inflow'
    value_2 = 'outflow'
    value_3 = 'excess_heat'
    value_4 = 'supply_heat'