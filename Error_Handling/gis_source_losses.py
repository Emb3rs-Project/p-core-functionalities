from pydantic import BaseModel, NonNegativeFloat, validator



class GISSourceLosses(BaseModel):

    source_id: int
    losses_total: NonNegativeFloat

