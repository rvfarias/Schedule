from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    max_period_per_person = Column(Integer, nullable=False)
    people = relationship("Person", back_populates="schedule")
    days = relationship("ScheduleDay", back_populates="schedule", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="schedule", cascade="all, delete-orphan")

