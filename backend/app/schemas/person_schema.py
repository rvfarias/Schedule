from pydantic import BaseModel
from typing import List

class PersonBase(BaseModel):
    name: str
    last_name: str
    availability: List[int]  # JSON string representing availability

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int

    class Config:
        orm_mode = True