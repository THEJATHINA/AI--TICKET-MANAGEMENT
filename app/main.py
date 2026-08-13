from fastapi import FastAPI

from . import models
from .database import engine

# Create all database tables from the SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupportPilot - Database Foundation",
    description="Backend foundation created by Member 1",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "SupportPilot Database Foundation is running",
        "status": "Connected to MySQL",
        "database": "supportpilot"
    }