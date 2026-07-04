import joblib
import os
from typing import Tuple, Dict
from config import SEVERITY_MODEL_PATH, SEVERITY_VECTORIZER_PATH

class SeverityPredictor:
    def __init__(self):
        # Load the models lazily or upon initialization
        if not os.path.exists(SEVERITY_MODEL_PATH) or not os.path.exists(SEVERITY_VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Severity models not found. Please run train_model.py first."
            )
        self.model = joblib.load(SEVERITY_MODEL_PATH)
        self.vectorizer = joblib.load(SEVERITY_VECTORIZER_PATH)
        
    def predict(self, cleaned_text: str) -> Tuple[str, Dict[str, float]]:
        """
        Predicts severity for preprocessed text.
        Returns:
            Tuple of (predicted_class, class_probabilities)
        """
        # Vectorize input text
        vec_text = self.vectorizer.transform([cleaned_text])
        
        # Predict class
        pred = self.model.predict(vec_text)[0]
        
        # Get probability distributions
        probs = self.model.predict_proba(vec_text)[0]
        class_probs = {cls: float(prob) for cls, prob in zip(self.model.classes_, probs)}
        
        return pred, class_probs
