from pydantic import BaseModel, Field

class TicketInput(BaseModel):
    subject: str = Field(..., min_length=1, description="Subject of the support ticket", examples=["VPN connection down"])
    description: str = Field(..., min_length=1, description="Detailed description of the support ticket", examples=["I cannot connect to the VPN from home since this morning."])

class PredictionOutput(BaseModel):
    severity: str = Field(..., description="Predicted severity level (Low, Medium, High)")
    priority: str = Field(..., description="Predicted priority level (P1, P2, P3, P4)")
    severity_confidence: float = Field(..., description="Confidence score for severity prediction (0.0 to 100.0)")
    priority_confidence: float = Field(..., description="Confidence score for priority prediction (0.0 to 100.0)")
    overall_confidence: float = Field(..., description="Overall consolidated confidence score (0.0 to 100.0)")
