from fastapi import APIRouter, HTTPException

from schemas import TicketInput, PredictionOutput
from predictor import TicketPredictor

router = APIRouter(prefix="/api/v1", tags=["Predictions"])

# Initialize predictor once at startup
try:
    predictor = TicketPredictor()
except Exception as e:
    # If models haven't been trained yet, keep it None but don't crash startup
    # (though they should be trained)
    print(f"Warning: Predictor failed to load: {e}")
    predictor = None

@router.post("/predict", response_model=PredictionOutput)
def predict_severity_priority(ticket: TicketInput):
    """
    Predict the Severity, Priority, and Confidence scores of an incoming IT support ticket
    based on its Subject and Description.
    """
    global predictor
    if predictor is None:
        # Try to initialize again (in case models were trained after startup)
        try:
            predictor = TicketPredictor()
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Model files not found or failed to load: {str(e)}. Please ensure models are trained."
            )
            
    try:
        result = predictor.predict_ticket(ticket.subject, ticket.description)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )
