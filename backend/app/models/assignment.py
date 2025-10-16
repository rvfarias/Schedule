from sqlalchemy import Column, Integer, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period = Column(String)  # e.g., "morning", "afternoon", "evening"
    person_ids = Column(JSON)  # Comma-separated list of person IDs
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="assignments")