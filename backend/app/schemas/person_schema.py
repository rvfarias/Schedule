from pydantic import BaseModel
from typing import List
from .availability_schema import AvailabilityBase

class PersonBase(BaseModel):
    name: str
    last_name: str
    availability: List[AvailabilityBase]  

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int
    schedule_id: int

    class Config:
        from_attributes = True