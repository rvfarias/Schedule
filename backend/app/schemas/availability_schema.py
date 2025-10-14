from pydantic import BaseModel
from typing import List

class AvailabilityBase(BaseModel):
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period: List[str]  # e.g., "morning", "afternoon", "evening"

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True