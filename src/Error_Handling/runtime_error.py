from dataclasses import dataclass


@dataclass
class ModuleException(Exception):
    code: str
    msg: str


@dataclass
class ModuleRuntimeException(ModuleException):
    type: str

    def __post_init__(self):
        raise TypeError(self.msg, 'code=' + self.code, 'type:' + self.type)
