from pydantic import BaseModel

class Availability(BaseModel):
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period: str  # e.g., "morning", "afternoon", "evening"

class AvailabilityCreate(Availability):
    pass

class AvailabilityResponse(Availability):
    id: int
    person_id: int

    class Config:
        orm_mode = True