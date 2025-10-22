from pydantic import BaseModel
from typing import List

class ScheduleDayBase(BaseModel):
    day: int
    people_per_period: List[int]
    period: List[str]

class ScheduleDayCreate(ScheduleDayBase):
    pass

class ScheduleDayResponse(ScheduleDayBase):
    id: int
    schedule_id: int

    class Config:
        from_attributes = True