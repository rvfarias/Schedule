from pydantic import BaseModel
from typing import List
from .availability_schema import Availability

class PersonBase(BaseModel):
    name: str
    last_name: str
    availability: List[Availability]  # JSON string representing availability

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int

    class Config:
        orm_mode = True