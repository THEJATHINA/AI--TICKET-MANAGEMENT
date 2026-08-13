"""
Milestone 3 - Member 5 (RAG / LLM Engineer)

LLM Configuration

This module initializes the Groq Large Language Model
used by the Resolution Agent.

Configuration is loaded from environment variables.

Environment Variables
---------------------
GROQ_API_KEY
    API key for Groq.

GROQ_MODEL
    Groq model name.
    Default:
        llama-3.3-70b-versatile

GROQ_TEMPERATURE
    Sampling temperature.
    Default:
        0.0

Exports
-------
llm
    Initialized ChatGroq client.
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GROQ_TEMPERATURE = float(
    os.getenv(
        "GROQ_TEMPERATURE",
        "0.0",
    )
)

# ---------------------------------------------------
# Validation
# ---------------------------------------------------

if not GROQ_API_KEY:

    logger.error(
        "GROQ_API_KEY environment variable is missing."
    )

    raise ValueError(
        "GROQ_API_KEY is not set in the environment."
    )

if not 0.0 <= GROQ_TEMPERATURE <= 2.0:

    logger.error(
        "Invalid GROQ_TEMPERATURE: %.2f",
        GROQ_TEMPERATURE,
    )

    raise ValueError(
        "GROQ_TEMPERATURE must be between 0.0 and 2.0."
    )

# ---------------------------------------------------
# Initialize Groq LLM
# ---------------------------------------------------

try:

    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=GROQ_TEMPERATURE,
        api_key=GROQ_API_KEY,
    )

    logger.info(
        "Groq model initialized successfully: %s",
        GROQ_MODEL,
    )

except Exception as exc:

    logger.exception(
        "Failed to initialize Groq LLM."
    )

    raise RuntimeError(
        "Unable to initialize the Groq LLM."
    ) from exc

# ---------------------------------------------------
# Public Exports
# ---------------------------------------------------

__all__ = ["llm"]