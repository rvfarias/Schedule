from pydantic import BaseModel
from typing import List
from .person_schema import PersonBase
from .assignment_schema import AssignmentBase

class ScheduleBase(BaseModel):
    days: int
    period: List[str]  # e.g., "morning", "afternoon",
    month: str
    year: str
    people: List[PersonBase]
    assignments: List[AssignmentBase]


class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        orm_mode = True