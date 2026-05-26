from pydantic import BaseModel
from typing import List, Dict, Optional
from app.schemas import person_schema
from app.schemas import schedule_day_schema


class ScheduleBase(BaseModel):
    days: List[schedule_day_schema.ScheduleDayBase]
    month: str
    year: int
    max_period_per_person: int
    people: List[person_schema.PersonBase]
    assignments: Optional[Dict[int, Dict[str, List[int]]]] = None


class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    people: List[person_schema.PersonResponse]

    class Config:
        """
        Enables ORM mode so that Pydantic can work seamlessly with ORM objects.
        """
        from_attributes = True