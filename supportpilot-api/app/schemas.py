from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
 
 
class TicketCreate(BaseModel):
    """What the frontend form sends us."""
    subject: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    requester_email: EmailStr
    department: Optional[str] = None
 
 
class TicketResponse(BaseModel):
    """What we send back after creating a ticket."""
    ticket_id: int
    user_id: int
    subject: str
    description: str
    priority: str
    severity: str
    status: str
    created_at: datetime
 
    class Config:
        from_attributes = True