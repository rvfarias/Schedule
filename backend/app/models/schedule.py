from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    period = Column(JSON, nullable=False)  # e.g., "morning", "afternoon", "evening"
    min_people_per_shift = Column(Integer, nullable=False)
    max_people_per_shift = Column(Integer, nullable=False)
    people = relationship("Person", back_populates="schedule")
    assignments = relationship("Assignment", back_populates="schedule", cascade="all, delete-orphan")

