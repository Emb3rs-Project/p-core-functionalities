from enum import Enum


class ConsumerTypeOptions(str, Enum):
    value_1 = 'household'
    value_2 = 'non-household'