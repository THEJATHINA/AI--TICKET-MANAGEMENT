from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from routes import predict

app = FastAPI(
    title="Severity & Priority Scoring API",
    description="Microservice to predict IT ticket severity (Low/Med/High) and priority (P1-P4) using machine learning.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prediction router
app.include_router(predict.router)

@app.get("/", include_in_schema=False)
def root_redirect():
    """
    Redirect the root URL to the interactive Swagger documentation.
    """
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
