from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schedule import Schedule
from app.models.person import Person
from app.models.schedule_day import ScheduleDay
from app.models.availability import Availability
from app.schemas import schedule_schema
from app.services.schedule_generator import generate_schedule as generate_schedule_service

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/", response_model=schedule_schema.ScheduleResponse)
def create_schedule(schedule: schedule_schema.ScheduleCreate, db: Session = Depends(get_db)):
    """Create a new schedule with nested days and people."""

    days_objs = []
    for d in schedule.days:
        day_objs = ScheduleDay(
            day=d.day,
            people_per_period=d.people_per_period,
            period=d.period
        )
        days_objs.append(day_objs)

    people_objs = []
    for person_data in schedule.people:
        person_obj = Person(
            name=person_data.name,
            last_name=person_data.last_name
        )
        db.add(person_obj)
        db.flush()  # Assigns an id to person_obj
        availability_objs = [Availability(**a.dict(), person_id=person_obj.id) for a in person_data.availability]
        person_obj.availability = availability_objs
        people_objs.append(person_obj)
        
    new_schedule = Schedule(
        month=schedule.month,
        year=schedule.year,
        max_period_per_person=schedule.max_period_per_person,
        days=days_objs,
        people=people_objs
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

@router.put("/{schedule_id}", response_model=schedule_schema.ScheduleResponse)
def update_schedule(schedule_id: int, updated_schedule: schedule_schema.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    db_schedule.month = updated_schedule.month
    db_schedule.year = updated_schedule.year
    db_schedule.max_period_per_person = updated_schedule.max_period_per_person
    del db_schedule.days[:]
    del db_schedule.people[:]
    db.flush()

    db_schedule.days = []
    for d in updated_schedule.days:
        day_obj = ScheduleDay(**d.dict(), schedule_id=db_schedule.id)
        db_schedule.days.append(day_obj)

    people_objs = []
    for person_data in updated_schedule.people:
        person_obj = Person(
            name=person_data.name,
            last_name=person_data.last_name
        )
        db.add(person_obj)
        db.flush()  # Assigns an id to person_obj
        availability_objs = [Availability(**a.dict(), person_id=person_obj.id) for a in person_data.availability]
        person_obj.availability = availability_objs
        people_objs.append(person_obj)
        db_schedule.people = people_objs
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=list[schedule_schema.ScheduleResponse])
def list_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()

@router.get("/{schedule_id}", response_model=schedule_schema.ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    if not schedule_id:
        return HTTPException(status_code=400, detail="Invalid schedule ID")
    
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

@router.post("/{schedule_id}/generate", response_model=schedule_schema.ScheduleResponse)
def generate_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    people = db_schedule.people
    days = db_schedule.days

    schedule_data = schedule_schema.ScheduleBase(
        days=[
            {
                "day": d.day,
                "people_per_period": d.people_per_period,
                "period": d.period
            }for d in days
        ]
        ,
        people=[
            {
                "name": p.name,
                "last_name": p.last_name,
                "availability": [
                    {
                        "day": a.day,
                        "period": a.period
                    } for a in p.availability
                ]
            } for p in people
        ],
        month=db_schedule.month,
        year=db_schedule.year,
        max_period_per_person=db_schedule.max_period_per_person
    )

    generated_schedule = generate_schedule_service(schedule_data)
    db_schedule.assignments = generated_schedule
    db.commit()
    db.refresh(db_schedule)

    return db_schedule
