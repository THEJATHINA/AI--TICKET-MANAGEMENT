"""
Milestone 3 - Member 5 (RAG / LLM Engineer)

Escalation Agent

Determines whether a support ticket should
be escalated after the Resolution Agent
completes troubleshooting.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Configurable Threshold
# ---------------------------------------------------

CONFIDENCE_THRESHOLD = 0.75


class EscalationAgent:
    """
    Determines whether a ticket should be
    escalated after the Resolution Agent
    completes troubleshooting.

    Inputs
    ------
    ticket
        Original user ticket.

    diagnosis_output
        Output returned by the Diagnosis Agent.

    resolution_output
        Output returned by the Resolution Agent.

    Returns
    -------
    {
        "escalate": bool,
        "escalate_to": str | None,
        "reason": str | None,
    }
    """

    @staticmethod
    def run(
        ticket: str,
        diagnosis_output: dict[str, Any],
        resolution_output: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Determine whether escalation is required.
        """

        logger.info("Escalation Agent started.")

        confidence = float(
            resolution_output.get("confidence", 0.0)
        )

        success = bool(
            resolution_output.get("success", False)
        )

        priority = diagnosis_output.get(
            "suggested_priority",
            "Medium",
        ).strip()

        # ---------------------------------------------------
        # Resolution generation failed
        # ---------------------------------------------------

        if not success:

            logger.warning(
                "Resolution generation failed. Escalating."
            )

            return {
                "escalate": True,
                "escalate_to": "IT Support Team",
                "reason": (
                    "The Resolution Agent could not generate "
                    "a valid troubleshooting response."
                ),
            }

        # ---------------------------------------------------
        # Low confidence
        # ---------------------------------------------------

        if confidence < CONFIDENCE_THRESHOLD:

            logger.info(
                "Low confidence (%.2f). Escalating.",
                confidence,
            )

            return {
                "escalate": True,
                "escalate_to": "IT Support Team",
                "reason": (
                    "The generated resolution has a low "
                    f"confidence score ({confidence:.2f}) "
                    "and requires manual review."
                ),
            }

        # ---------------------------------------------------
        # Critical priority ticket
        # ---------------------------------------------------

        if priority.lower() == "critical":

            logger.info(
                "Critical priority ticket detected."
            )

            return {
                "escalate": True,
                "escalate_to": "IT Support Team",
                "reason": (
                    "Critical-priority incidents require "
                    "manual review by the IT Support Team."
                ),
            }

        # ---------------------------------------------------
        # No escalation required
        # ---------------------------------------------------

        logger.info(
            "Ticket resolved successfully without escalation "
            "(confidence=%.2f).",
            confidence,
        )

        return {
            "escalate": False,
            "escalate_to": None,
            "reason": (
                "The issue can be handled using the "
                "generated troubleshooting guidance."
            ),
        }