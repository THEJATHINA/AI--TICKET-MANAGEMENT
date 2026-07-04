import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import joblib

data = pd.read_csv("sample_tickets_350.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["text"])
y = data["category"]

base_model = LinearSVC()
model = CalibratedClassifierCV(base_model, cv=5)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Final model trained on all 350 tickets and saved!")