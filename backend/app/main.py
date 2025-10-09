from fastapi import FastAPI
from app.routers import people
from app.routers import schedules
from app.core.database import Base, engine

# Cria as tabelas do banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestão de Escalas da Igreja",
    description="API para gerenciamento de escalas de ministérios",
    version="1.0.0",
)

# Inclui as rotas
app.include_router(people.router)
app.include_router(schedules.router)

@app.get("/")
def root():
    return {"message": "API de Escalas da Igreja está rodando 🚀"}
