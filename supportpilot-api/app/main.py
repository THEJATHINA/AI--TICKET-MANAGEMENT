from datetime import datetime
from typing import Generator

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./supportpilot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    description = Column(String(4000), nullable=False)
    category = Column(String(100), nullable=False, default="Unknown")
    severity = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SupportPilot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketCreate(BaseModel):
    subject: str
    description: str
    severity: str
    priority: str
    status: str | None = None


class TicketResponse(BaseModel):
    ticket_id: int
    subject: str
    description: str
    category: str
    severity: str
    priority: str
    confidence: float
    status: str
    created_at: datetime


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def classify_ticket(description: str) -> tuple[str, float]:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/classify",
            json={"text": description},
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()
        category = str(payload.get("category") or "Unknown")
        confidence = float(payload.get("confidence", 0) or 0)
        return category, confidence
    except (requests.RequestException, ValueError, TypeError):
        return "Unknown", 0.0


@app.post("/api/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    db = SessionLocal()
    try:
        category, confidence = classify_ticket(ticket.description)
        db_ticket = Ticket(
            subject=ticket.subject,
            description=ticket.description,
            category=category,
            severity=ticket.severity,
            priority=ticket.priority,
            confidence=confidence,
            status=ticket.status or "Open",
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    finally:
        db.close()


@app.get("/api/tickets", response_model=list[TicketResponse])
def list_tickets():
    db = SessionLocal()
    try:
        tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
        return tickets
    finally:
        db.close()


@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    finally:
        db.close()
