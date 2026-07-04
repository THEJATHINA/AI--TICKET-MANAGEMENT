import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load your data
data = pd.read_csv("sample_tickets_350.csv")

# 2. Split into training (80%) and testing (20%) BEFORE doing anything else
X_train_text, X_test_text, y_train, y_test = train_test_split(
    data["text"],
    data["category"],
    test_size=0.2,        # 20% held out for testing
    random_state=42,       # keeps the split the same every time you run it
    stratify=data["category"]  # keeps categories balanced in both splits
)

# 3. Turn text into numbers — fit ONLY on training data
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)   # just transform, don't fit again

# 4. Train the model on training data only
model = LinearSVC()
model.fit(X_train, y_train)

# 5. Test the model on data it has NEVER seen
y_pred = model.predict(X_test)

# 6. Print the actual accuracy number
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on test data: {accuracy * 100:.2f}%")

# 7. (Bonus) Detailed breakdown per category
print("\nDetailed report:")
print(classification_report(y_test, y_pred))

# 8. Save the model — but note: this is trained only on 80% of data
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel trained and saved!")