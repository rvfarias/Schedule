from pydantic import BaseModel
from typing import List

class AvailabilityBase(BaseModel):
    day: int 
    period: List[str]  # e.g., "morning", "afternoon", "evening"

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True