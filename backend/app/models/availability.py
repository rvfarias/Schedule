from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)  # 0=Sunday, 1=Monday, ..., 6=Saturday
    period = Column(JSON, nullable=False)  # e.g., "morning", "afternoon", "evening"
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    person = relationship("Person", back_populates="availability")