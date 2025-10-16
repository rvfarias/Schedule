from pydantic import BaseModel
from typing import List

class AssignmentBase(BaseModel):
    day: int  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period: str  # e.g., "morning", "afternoon", "evening"
    person_ids: List[int]  # List of person IDs assigned to this period

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    schedule_id: int

    class Config:
        orm_mode = True


