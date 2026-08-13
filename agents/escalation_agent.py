"""
Milestone 3 - Member 5 (RAG / LLM Engineer)

Escalation Agent

Determines whether an AI-generated resolution
should be escalated to human support.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

MIN_CONFIDENCE = 0.70

HIGH_PRIORITY = {"P1"}

HIGH_SEVERITY = {"CRITICAL"}

# Escalate only if the LLM explicitly recommends
# contacting human support.
ESCALATION_PHRASES = [
    "contact it support",
    "contact support",
    "contact your administrator",
    "contact the administrator",
    "contact your system administrator",
    "human support",
    "level 2 support",
    "please escalate",
    "requires escalation",
]


class EscalationAgent:
    """
    Determines whether a support ticket should be
    escalated after AI resolution.
    """

    def run(
        self,
        resolution_output: dict[str, Any],
        diagnosis_output: dict[str, Any],
    ) -> dict[str, Any]:

        logger.info("Escalation Agent started.")

        try:

            confidence = resolution_output.get(
                "confidence",
                0.0,
            )

            success = resolution_output.get(
                "success",
                False,
            )

            priority = diagnosis_output.get(
                "suggested_priority",
                "P4",
            )

            severity = diagnosis_output.get(
                "severity",
                "LOW",
            )

            resolution_text = (
                resolution_output.get(
                    "resolution_steps",
                    "",
                )
                .lower()
                .strip()
            )

            # -----------------------------------------
            # Rule 1
            # Resolution generation failed
            # -----------------------------------------

            if not success:

                logger.info(
                    "Escalating because AI resolution failed."
                )

                return {
                    "escalated": True,
                    "assigned_team": "Level 2 Support",
                    "reason": "Resolution generation failed.",
                    "status": "OPEN",
                }

            # -----------------------------------------
            # Rule 2
            # Low confidence
            # -----------------------------------------

            if confidence < MIN_CONFIDENCE:

                logger.info(
                    "Escalating because confidence %.2f < %.2f",
                    confidence,
                    MIN_CONFIDENCE,
                )

                return {
                    "escalated": True,
                    "assigned_team": "Level 2 Support",
                    "reason": (
                        f"Low AI confidence ({confidence:.2f})."
                    ),
                    "status": "OPEN",
                }

            # -----------------------------------------
            # Rule 3
            # Critical Priority
            # -----------------------------------------

            if priority in HIGH_PRIORITY:

                logger.info(
                    "Escalating because priority=%s",
                    priority,
                )

                return {
                    "escalated": True,
                    "assigned_team": "Priority Support",
                    "reason": (
                        f"Priority {priority} requires review."
                    ),
                    "status": "OPEN",
                }

            # -----------------------------------------
            # Rule 4
            # Critical Severity
            # -----------------------------------------

            if severity in HIGH_SEVERITY:

                logger.info(
                    "Escalating because severity=%s",
                    severity,
                )

                return {
                    "escalated": True,
                    "assigned_team": "Critical Incident Team",
                    "reason": "Critical severity issue.",
                    "status": "OPEN",
                }

            # -----------------------------------------
            # Rule 5
            # Explicit LLM recommendation
            # -----------------------------------------

            matched_phrase = next(
                (
                    phrase
                    for phrase in ESCALATION_PHRASES
                    if phrase in resolution_text
                ),
                None,
            )

            if matched_phrase:

                logger.info(
                    "Escalating because LLM suggested '%s'.",
                    matched_phrase,
                )

                return {
                    "escalated": True,
                    "assigned_team": "Level 2 Support",
                    "reason": (
                        "LLM recommended human escalation."
                    ),
                    "status": "OPEN",
                }

            # -----------------------------------------
            # Ticket resolved automatically
            # -----------------------------------------

            logger.info(
                "Ticket resolved automatically."
            )

            return {
                "escalated": False,
                "assigned_team": None,
                "reason": None,
                "status": "RESOLVED",
            }

        except Exception as exc:

            logger.exception(
                "Escalation Agent failed."
            )

            return {
                "escalated": True,
                "assigned_team": "Level 2 Support",
                "reason": str(exc),
                "status": "OPEN",
            }


__all__ = [
    "EscalationAgent",
]