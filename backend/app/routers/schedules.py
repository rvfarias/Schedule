from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schedule import Schedule
from app.models.person import Person
from app.models.availability import Availability
from app.schemas import schedule_schema


router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/", response_model=schedule_schema.ScheduleResponse)
def create_schedule(schedule: schedule_schema.ScheduleCreate, db: Session = Depends(get_db)):
    """
    Create a new schedule with associated people and their availability.

    Args:
        schedule (schedule_schema.ScheduleCreate): The schedule data including people and their availability.
        db (Session, optional): The database session dependency.

    Returns:
        schedule.Schedule: The newly created schedule object.
    """
    people_objs = []
    for person_data in schedule.people:
        availability_objs = [Availability(**a.dict()) for a in person_data.availability]
        person_obj = Person(
            name=person_data.name,
            last_name=person_data.last_name,
            availability=availability_objs
        )
        people_objs.append(person_obj)
        
    new_schedule = Schedule(
        month=schedule.month,
        year=schedule.year,
        people=people_objs
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


@router.get("/", response_model=list[schedule_schema.ScheduleResponse])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()

@router.get("/{schedule_id}", response_model=schedule_schema.ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    if not schedule_id:
        return HTTPException(status_code=400, detail="Invalid schedule ID")
    
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

