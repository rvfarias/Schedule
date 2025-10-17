from pydantic import BaseModel
from typing import List, Dict
from .person_schema import PersonBase
from .schedule_day_schema import ScheduleDayBase

class ScheduleBase(BaseModel):
    days: List[ScheduleDayBase]
    month: str
    year: int
    max_period_per_person: int
    people: List[PersonBase]
    assignments: Dict[int, Dict[str, List[int]]] | None = None


class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        orm_mode = True