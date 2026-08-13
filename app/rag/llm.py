import logging
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)
GROQ_TEMPERATURE = float(
    os.getenv("GROQ_TEMPERATURE", "0")
)

# ---------------------------------------------------
# Validation
# ---------------------------------------------------

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY is missing.")
    raise ValueError(
        "GROQ_API_KEY is not set in the environment."
    )

# ---------------------------------------------------
# Initialize Groq LLM
# ---------------------------------------------------

try:
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=GROQ_TEMPERATURE,
    )

    logger.info(f"Groq model initialized: {GROQ_MODEL}")

except Exception as e:
    logger.exception("Failed to initialize Groq model.")
    raise RuntimeError(
        "Unable to initialize Groq LLM."
    ) from e