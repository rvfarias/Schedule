from fastapi  import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import person as models
from app.schemas import person_schema as schemas

router = APIRouter(prefix="/people", tags=["people"])

@router.post("/", response_model=schemas.PersonResponse)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    new_person = models.Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@router.get("/", response_model=list[schemas.PersonResponse])
def list_people(db: Session = Depends(get_db)):
    return db.query(models.Person).all()