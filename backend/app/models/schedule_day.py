from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScheduleDay(Base):
    __tablename__ = "schedule_days"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period = Column(JSON, nullable=False)  # e.g., "morning", "afternoon", "evening"
    people_per_period = Column(JSON, nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="days")