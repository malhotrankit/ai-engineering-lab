from decimal import Decimal

import pytest
from pydantic import ValidationError

from ai_engineering_lab.earnings_models import EarningsExtraction
from ai_engineering_lab.fake_extractor import extract_earnings_fake, verify_evidence


def test_extract_earnings_fake_valid() -> None:
    text = "Tesla reported Q2 2025 revenue of $25.2 billion USD. Guidance was strong growth. Risks include competition."
    result = extract_earnings_fake(text)

    # 1. Verify schema validation passes
    extraction = EarningsExtraction(**result)
    assert extraction.company == "Tesla"
    assert extraction.reporting_period == "Q2 2025"
    assert len(extraction.metrics) == 1
    assert extraction.metrics[0].name == "Revenue"
    assert extraction.metrics[0].value == Decimal("25.2")
    assert extraction.metrics[0].unit == "billion USD"

    # 2. Verify grounding check passes
    assert verify_evidence(result, text) is True
    assert verify_evidence(extraction, text) is True


def test_extract_earnings_fake_malformed() -> None:
    text = "This input contains malformed text."
    result = extract_earnings_fake(text)

    # 1. Verify schema validation fails
    with pytest.raises(ValidationError) as exc_info:
        EarningsExtraction(**result)

    assert "reporting_period" in str(exc_info.value)


def test_extract_earnings_fake_ungrounded() -> None:
    text = "This is ungrounded data for Apple's earnings."
    result = extract_earnings_fake(text)

    # 1. Verify schema validation passes
    extraction = EarningsExtraction(**result)
    assert extraction.company == "Ungrounded LLC"

    # 2. Verify grounding check fails
    assert verify_evidence(result, text) is False
    assert verify_evidence(extraction, text) is False
