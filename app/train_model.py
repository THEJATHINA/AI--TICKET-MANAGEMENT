import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from preprocess import prepare_input

def train():
    # Define paths
    dataset_path = os.path.join("dataset", "tickets.csv")
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    # Load dataset
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")
        
    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df)} samples from {dataset_path}")
    
    # Preprocess text
    df["cleaned_text"] = df.apply(lambda row: prepare_input(row["subject"], row["description"]), axis=1)
    
    # Target columns
    X = df["cleaned_text"].values
    y_sev = df["severity"].values
    y_pri = df["priority"].values
    
    # --- 1. Severity Model ---
    print("\n--- Training Severity Model ---")
    X_train_sev, X_test_sev, y_train_sev, y_test_sev = train_test_split(
        X, y_sev, test_size=0.2, random_state=42, stratify=y_sev
    )
    
    sev_vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X_train_sev_vec = sev_vectorizer.fit_transform(X_train_sev)
    X_test_sev_vec = sev_vectorizer.transform(X_test_sev)
    
    # Use Logistic Regression with probability calculation enabled
    sev_model = LogisticRegression(max_iter=1000, random_state=42)
    sev_model.fit(X_train_sev_vec, y_train_sev)
    
    # Evaluate Severity
    y_pred_sev = sev_model.predict(X_test_sev_vec)
    sev_acc = accuracy_score(y_test_sev, y_pred_sev)
    print(f"Severity Prediction Accuracy: {sev_acc:.4f} ({sev_acc*100:.2f}%)")
    print(classification_report(y_test_sev, y_pred_sev))
    
    # Save severity model & vectorizer
    joblib.dump(sev_model, os.path.join(models_dir, "severity_model.pkl"))
    joblib.dump(sev_vectorizer, os.path.join(models_dir, "severity_vectorizer.pkl"))
    print("Saved severity model and vectorizer.")
    
    # --- 2. Priority Model ---
    print("\n--- Training Priority Model ---")
    X_train_pri, X_test_pri, y_train_pri, y_test_pri = train_test_split(
        X, y_pri, test_size=0.2, random_state=42, stratify=y_pri
    )
    
    pri_vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X_train_pri_vec = pri_vectorizer.fit_transform(X_train_pri)
    X_test_pri_vec = pri_vectorizer.transform(X_test_pri)
    
    pri_model = LogisticRegression(max_iter=1000, random_state=42)
    pri_model.fit(X_train_pri_vec, y_train_pri)
    
    # Evaluate Priority
    y_pred_pri = pri_model.predict(X_test_pri_vec)
    pri_acc = accuracy_score(y_test_pri, y_pred_pri)
    print(f"Priority Prediction Accuracy: {pri_acc:.4f} ({pri_acc*100:.2f}%)")
    print(classification_report(y_test_pri, y_pred_pri))
    
    # Save priority model & vectorizer
    joblib.dump(pri_model, os.path.join(models_dir, "priority_model.pkl"))
    joblib.dump(pri_vectorizer, os.path.join(models_dir, "priority_vectorizer.pkl"))
    print("Saved priority model and vectorizer.")
    
    return sev_acc, pri_acc

if __name__ == "__main__":
    train()
