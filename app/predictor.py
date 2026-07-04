from preprocess import prepare_input
from severity import SeverityPredictor
from priority import PriorityPredictor
from confidence import get_class_confidence, calculate_overall_confidence
from schemas import PredictionOutput

class TicketPredictor:
    def __init__(self):
        # Initialize sub-predictors
        self.severity_predictor = SeverityPredictor()
        self.priority_predictor = PriorityPredictor()

    def predict_ticket(self, subject: str, description: str) -> PredictionOutput:
        """
        Runs the full prediction pipeline:
        1. Cleans and preprocesses the combined subject and description.
        2. Predicts severity and fetches its confidence.
        3. Predicts priority and fetches its confidence.
        4. Calculates overall confidence.
        5. Returns the consolidated PredictionOutput.
        """
        # Clean text
        cleaned_text = prepare_input(subject, description)
        
        # Predict Severity
        sev_label, sev_probs = self.severity_predictor.predict(cleaned_text)
        sev_conf = get_class_confidence(sev_label, sev_probs)
        
        # Predict Priority
        pri_label, pri_probs = self.priority_predictor.predict(cleaned_text)
        pri_conf = get_class_confidence(pri_label, pri_probs)
        
        # Calculate overall confidence
        overall_conf = calculate_overall_confidence(sev_conf, pri_conf)
        
        return PredictionOutput(
            severity=sev_label,
            priority=pri_label,
            severity_confidence=sev_conf,
            priority_confidence=pri_conf,
            overall_confidence=overall_conf
        )
