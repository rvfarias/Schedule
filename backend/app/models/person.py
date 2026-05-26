from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="people")
    availability = relationship("Availability", back_populates="person", cascade="all, delete-orphan")
  