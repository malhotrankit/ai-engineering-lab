from typing import Any

from ai_engineering_lab.earnings_models import EarningsExtraction


def extract_earnings_fake(text: str) -> dict[str, Any]:
    """
    Fake extractor to simulate LLM JSON output for earnings extraction.
    Returns structurally valid, malformed, or ungrounded data based on the input text.

    Rules:
    1. If "malformed" is in text.lower(), return a dictionary missing a required field (like reporting_period).
    2. If "ungrounded" is in text.lower(), return a dictionary that matches the schema perfectly, but has fabricated data.
    3. Otherwise, return a valid, realistic dictionary based on the text.
    """
    text_lower = text.lower()

    if "malformed" in text_lower:
        # Missing required field 'reporting_period'
        return {
            "company": "Fake Corp",
            "metrics": [
                {
                    "name": "Revenue",
                    "value": "100.0",
                    "unit": "USD",
                    "evidence": "Fake Corp made 100 USD.",
                }
            ],
            "guidance": "Growth expected.",
            "risks": ["Competition"],
        }

    if "ungrounded" in text_lower:
        # Matches schema perfectly but has fabricated data (evidence not in text)
        return {
            "company": "Ungrounded LLC",
            "reporting_period": "Q4 2025",
            "metrics": [
                {
                    "name": "Net Income",
                    "value": "50.0",
                    "unit": "million USD",
                    "evidence": "This sentence is completely fabricated and is not in the source text.",
                }
            ],
            "guidance": "No guidance provided.",
            "risks": ["Fabricated risk"],
        }

    # Otherwise, return a valid, realistic dictionary based on the text.
    if "tesla" in text_lower:
        return {
            "company": "Tesla",
            "reporting_period": "Q2 2025",
            "metrics": [
                {
                    "name": "Revenue",
                    "value": "25.2",
                    "unit": "billion USD",
                    "evidence": "Tesla reported Q2 2025 revenue of $25.2 billion USD",
                }
            ],
            "guidance": "strong growth",
            "risks": ["competition"],
        }

    # Generic realistic fallback where evidence is a substring of the source text
    evidence_str = text if text else "No evidence available."
    return {
        "company": "Example Corp",
        "reporting_period": "Q2 2025",
        "metrics": [
            {
                "name": "Revenue",
                "value": "25.2",
                "unit": "billion USD",
                "evidence": evidence_str,
            }
        ],
        "guidance": None,
        "risks": [],
    }


def verify_evidence(
    extraction: dict[str, Any] | EarningsExtraction, source_text: str
) -> bool:
    """
    Verify that the evidence for each metric is a substring of the source text.
    """
    if isinstance(extraction, EarningsExtraction):
        metrics = extraction.metrics
        for metric in metrics:
            if not metric.evidence or metric.evidence not in source_text:
                return False
        return True
    elif isinstance(extraction, dict):
        metrics = extraction.get("metrics", [])
        if not metrics:
            return False
        for metric in metrics:
            evidence = metric.get("evidence")
            if not evidence or evidence not in source_text:
                return False
        return True
    return False
