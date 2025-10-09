from pydantic import BaseModel
from typing import List
from .person_schema import PersonBase

class ScheduleBase(BaseModel):
    month: str
    year: str
    people: List[PersonBase]

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        orm_mode = True