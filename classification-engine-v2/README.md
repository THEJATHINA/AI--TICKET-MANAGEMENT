# AI Ticket Classification — Real Dataset (Infosys AIML Project)

## About this dataset
Source: IT_Support_Ticket_Data.csv (real customer support tickets, 29,651 raw rows)

Cleaning steps applied:
1. Removed 1 row with missing ticket text
2. Fixed missing spaces after punctuation (e.g. "Team,I am" -> "Team, I am")
3. Removed 4,595 exact duplicate tickets
4. Removed junk/too-short rows (under 40 characters, e.g. "System", "Our system")
5. Cleaned the Tags column formatting
6. Merged overlapping departments into 5 clearer categories (see below)

## Why categories were merged
The original data had 10 departments (Technical Support, IT Support, Product
Support, Customer Service, Service Outages and Maintenance, General Inquiry,
Billing and Payments, Returns and Exchanges, Sales and Pre-Sales, Human
Resources). Testing showed the first six overlap heavily in real language
(a "Technical Support" ticket and an "IT Support" ticket often use nearly
identical words), so a model could not reliably tell them apart -- accuracy
was only ~50%.

These six were merged into a single "Technical Support" category, since
they represent genuinely similar types of tickets in this dataset. The
remaining four (Billing and Payments, Returns and Exchanges, Sales and
Pre-Sales, Human Resources) have distinct enough language to classify
separately.

Final categories used: Technical Support, Billing and Payments,
Returns and Exchanges, Sales and Pre-Sales, Human Resources

## Result
Accuracy on held-out test data: 89.46%

Honest note: "Technical Support" is a very large category (about 80% of
all tickets) and is classified very accurately (99% recall). The smaller
categories (Human Resources, Returns and Exchanges, Sales and Pre-Sales)
are harder to classify correctly due to having far fewer examples --
their recall is lower (25-37%). This is a realistic result for imbalanced
real-world data, and is worth explaining rather than hiding.

## Files in this project
- IT_Support_Ticket_Data_final.csv -> cleaned dataset with merged categories
- train_final_model.py             -> trains the model, prints accuracy report
- api.py                            -> FastAPI app exposing /classify endpoint

## Steps to run in VS Code

1. Open this folder in VS Code
2. Open a terminal (Terminal -> New Terminal)
3. Create a virtual environment:
   python -m venv venv
4. Activate it:
   Windows: venv\Scripts\activate
   Mac:     source venv/bin/activate
5. Install required packages:
   pip install pandas scikit-learn fastapi uvicorn joblib
6. Train the model:
   python train_final_model.py
7. Start the API:
   uvicorn api:app --reload
8. Test it in your browser:
   http://127.0.0.1:8000/docs
   Try POST /classify with:
   { "text": "I was charged twice for my subscription this month" }

## Endpoint
POST http://127.0.0.1:8000/classify

Request:
{ "text": "ticket description here" }

Response:
{ "category": "Billing and Payments", "confidence": 0.83 }

Categories: Technical Support, Billing and Payments, Returns and Exchanges,
Sales and Pre-Sales, Human Resources
