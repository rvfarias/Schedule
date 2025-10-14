from pydantic import BaseModel
from typing import List

class AssignmentBase(BaseModel):
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period: str  # e.g., "morning", "afternoon", "evening"
    person_id: int
    schedule_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        orm_mode = True


