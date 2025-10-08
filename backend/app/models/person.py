from sqlalchemy import Column, Integer, String, JSON
from app.core.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    availability = Column(JSON, nullable=False)