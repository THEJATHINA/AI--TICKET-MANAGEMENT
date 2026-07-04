import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Model files
SEVERITY_MODEL_PATH = os.path.join(MODELS_DIR, "severity_model.pkl")
SEVERITY_VECTORIZER_PATH = os.path.join(MODELS_DIR, "severity_vectorizer.pkl")

PRIORITY_MODEL_PATH = os.path.join(MODELS_DIR, "priority_model.pkl")
PRIORITY_VECTORIZER_PATH = os.path.join(MODELS_DIR, "priority_vectorizer.pkl")
