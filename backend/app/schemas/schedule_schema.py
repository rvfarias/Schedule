from pydantic import BaseModel
from typing import List, Dict, Optional
from .person_schema import PersonBase
from .schedule_day_schema import ScheduleDayBase

class ScheduleBase(BaseModel):
    days: List[ScheduleDayBase]
    month: str
    year: int
    max_period_per_person: int
    people: List[PersonBase]
    assignments: Optional[Dict[int, Dict[str, List[str]]]] = None


class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        """
        Enables ORM mode so that Pydantic can work seamlessly with ORM objects.
        """
        from_attributes = True