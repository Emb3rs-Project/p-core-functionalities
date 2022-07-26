from pydantic import BaseModel, NonNegativeFloat


class GISSourceLosses(BaseModel):
    source_id: int
    losses_total: NonNegativeFloat
