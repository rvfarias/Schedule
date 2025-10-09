from fastapi  import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.person import Person
from app.models.availability import Availability
from app.schemas import person_schema

router = APIRouter(prefix="/schedules/people", tags=["people"])


@router.put("/{schedule_id}/{person_id}", response_model=person_schema.PersonResponse)
def update_person(schedule_id: int, person_id: int, new_person: person_schema.PersonCreate, db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id, Person.schedule_id == schedule_id).first()    
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    db_person.name = new_person.name
    db_person.last_name = new_person.last_name

    db_person.availability.clear()
    db.flush()

    db_person.availability = [Availability(**a.dict()) for a in new_person.availability]
    db.commit()
    db.refresh(db_person)
    return db_person 


@router.get("/", response_model=list[person_schema.PersonResponse])
def list_people(db: Session = Depends(get_db)):
    return db.query(Person).all()