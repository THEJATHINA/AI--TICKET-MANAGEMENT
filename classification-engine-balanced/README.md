# AI Ticket Classification Engine (Member 4)

Classifies IT support tickets into 5 departments using TF-IDF + LinearSVC.

## Dataset
- File: balanced_it_tickets.csv
- 17,500 tickets, perfectly balanced (3,500 per department)
- Columns: Body, Department, Priority, Tags
- Departments: Technical Support, Billing and Payments,
  Returns and Exchanges, Sales and Pre-Sales, Human Resources

## Result
Accuracy on held-out test data: 93.43%
(No category scores 1.00 - realistic performance with vocabulary overlap)

Per-category: precision 0.92-0.94, recall 0.92-0.94, f1 0.93-0.94

## Files
- balanced_it_tickets.csv -> training dataset
- train_final_model.py     -> trains model, prints accuracy, saves model.pkl + vectorizer.pkl
- api.py                   -> FastAPI app exposing the /classify endpoint
- model.pkl / vectorizer.pkl -> the trained model (already generated)

## Steps to run in VS Code
1. Open this folder in VS Code
2. Open terminal (Terminal -> New Terminal)
3. Create a virtual environment:
   python -m venv venv
4. Activate it:
   Windows: venv\Scripts\activate
   Mac:     source venv/bin/activate
5. Install packages:
   pip install pandas scikit-learn fastapi uvicorn joblib
6. Train the model:
   python train_final_model.py
7. Start the API:
   uvicorn api:app --reload
8. Test in browser:
   http://127.0.0.1:8000/docs

## API / Integration details (for Member 6)

Endpoint:
POST http://127.0.0.1:8000/classify

Request JSON:
{
  "text": "ticket description here"
}

Response JSON:
{
  "department": "Technical Support",
  "confidence": 0.95
}

JSON field names:
- Request field:  "text"        (string - the ticket description)
- Response field: "department"  (string - one of the 5 departments)
- Response field: "confidence"  (number between 0 and 1)

Possible department values:
Technical Support, Billing and Payments, Returns and Exchanges,
Sales and Pre-Sales, Human Resources
