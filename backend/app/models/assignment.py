from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period = Column(String, nullable=False)  # e.g., "morning", "afternoon", "evening"
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    person = relationship("Person", back_populates="assignments")
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="assignments")