from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    max_period_per_person = Column(Integer, nullable=False)
    assignments = Column(JSON) # Armazena as atribuições como um campo JSON
    people = relationship("Person", back_populates="schedule", cascade="all, delete-orphan")
    days = relationship("ScheduleDay", back_populates="schedule", cascade="all, delete-orphan")
