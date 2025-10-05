from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.schedule_generator import ScheduleGeneratorService
from app import models, schemas

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/generate", response_model=schemas.ScheduleResponse)
def generate_schedule(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()
    days = db.query(models.Day).all()
    