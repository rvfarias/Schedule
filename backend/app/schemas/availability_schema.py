from pydantic import BaseModel
from typing import List

class Availability(BaseModel):
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period: List[str]  # e.g., "morning", "afternoon", "evening"

class AvailabilityCreate(Availability):
    pass

class AvailabilityResponse(Availability):
    id: int
    person_id: int

    class Config:
        orm_mode = True