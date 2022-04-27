from pydantic import BaseModel, validator, confloat, PositiveFloat,validate_arguments, conint, conlist




class Schedule(BaseModel):

    daily_periods: conlist(conlist(conint(ge=0, le=24), min_items=2, max_items=2), min_items=0)
    shutdown_periods: conlist(conlist(conint(ge=0, le=366), min_items=2, max_items=2), min_items=0)
    saturday_on: int
    sunday_on: int

    @validator('daily_periods')
    def check_structure_daily_periods(cls, v):
        if v != []:
            for value in v:
                if len(value) != 2:
                    raise ValueError('Only a start and ending hour must be given in each period. Example: [[9,12],[14,19]]')
                else:
                    value_a, value_b = value
                    if value_b <= value_a:
                        raise ValueError('Second value of the daily period must be larger than the first. Example: [[9,12],[14,19]]')
        return v


    @validator('shutdown_periods')
    def check_structure_shutdown_periods(cls, v):
        if v != []:
            for value in v:
                if len(value) != 2:
                    raise ValueError('Only a start and ending day must be given in each period. Example: [[220,250]]')
                else:
                    value_a, value_b = value
                    if value_b <= value_a:
                        raise ValueError('Second value of the shutdown period must be larger than the first. Example: [[220,250]]')
        return v





