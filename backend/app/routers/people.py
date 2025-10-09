from fastapi  import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import person
from app.models.availability import Availability
from app.schemas import person_schema

router = APIRouter(prefix="/people", tags=["people"])

@router.post("/", response_model=person_schema.PersonResponse)
def create_person(person: person_schema.PersonCreate, db: Session = Depends(get_db)):
    avaliability_objs =[
        Availability(**a.dict()) for a in person.availability
    ]

    new_person = person.Person(
        name=person.name,
        last_name=person.last_name,
        availability=avaliability_objs
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@router.put("/{person_id}", response_model=person_schema.PersonResponse)
def update_person(person_id: int, new_person: person_schema.PersonResponse, db: Session = Depends(get_db)):
    db_person = db.query(person.Person).filter(person.Person.id == person_id).first()
    
    if not db_person:
        return None
    
    db_person.name = new_person.name
    db_person.last_name = new_person.last_name
    db_person.availability = [Availability(**a.dict()) for a in new_person.availability]
    db.commit()
    db.refresh(db_person)
    return db_person 


@router.get("/", response_model=list[person_schema.PersonResponse])
def list_people(db: Session = Depends(get_db)):
    return db.query(person.Person).all()