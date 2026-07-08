import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the cleaned, categorized dataset
data = pd.read_csv("IT_Support_Ticket_Data_final.csv")

# Split into training (80%) and testing (20%)
X_train_text, X_test_text, y_train, y_test = train_test_split(
    data["text"],
    data["category"],
    test_size=0.2,
    random_state=42,
    stratify=data["category"]
)

# Convert text into numbers (using word pairs too, for better context)
vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)
X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

# Train the model (calibrated so it can give confidence scores)
base_model = LinearSVC()
model = CalibratedClassifierCV(base_model, cv=5)
model.fit(X_train, y_train)

# Test on unseen data
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on test data: {accuracy * 100:.2f}%")
print("\nDetailed report:")
print(classification_report(y_test, y_pred))

# Retrain on FULL dataset for the final production model
vectorizer_final = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)
X_full = vectorizer_final.fit_transform(data["text"])
y_full = data["category"]

final_base_model = LinearSVC()
final_model = CalibratedClassifierCV(final_base_model, cv=5)
final_model.fit(X_full, y_full)

joblib.dump(final_model, "model.pkl")
joblib.dump(vectorizer_final, "vectorizer.pkl")

print("\nFinal model trained on the full cleaned dataset and saved!")
