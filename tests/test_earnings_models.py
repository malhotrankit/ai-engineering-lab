from decimal import Decimal

import pytest
from pydantic import ValidationError

from ai_engineering_lab.earnings_models import EarningsExtraction, FinancialMetric


def test_financial_metric_accepts_valid_data() -> None:
    metric = FinancialMetric(
        name="Revenue",
        value=Decimal("25.2"),
        unit="billion USD",
        evidence="Revenue was $25.2 billion in Q2 2025.",
    )

    assert metric.name == "Revenue"
    assert metric.value == Decimal("25.2")


def test_extraction_accepts_valid_data() -> None:
    extraction = EarningsExtraction(
        company="Tesla",
        reporting_period="Q2 2025",
        metrics=[
            FinancialMetric(
                name="Revenue",
                value=Decimal("25.2"),
                unit="billion USD",
                evidence="Revenue was $25.2 billion in Q2 2025.",
            )
        ],
        guidance="Vehicle deliveries are expected to grow.",
        risks=["Demand uncertainty"],
    )

    assert extraction.company == "Tesla"
    assert len(extraction.metrics) == 1
    assert extraction.metrics[0].name == "Revenue"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("company", "   "),
        ("reporting_period", ""),
        ("metrics", []),
    ],
)
def test_extraction_rejects_invalid_required_data(
    field: str,
    value: object,
) -> None:
    valid_data = {
        "company": "Tesla",
        "reporting_period": "Q2 2025",
        "metrics": [
            {
                "name": "Revenue",
                "value": "25.2",
                "unit": "billion USD",
                "evidence": "Revenue was $25.2 billion in Q2 2025.",
            }
        ],
    }
    valid_data[field] = value

    with pytest.raises(ValidationError):
        EarningsExtraction(**valid_data)


def test_extraction_cleans_optional_fields() -> None:
    extraction = EarningsExtraction(
        company="  Tesla  ",
        reporting_period="  Q2 2025  ",
        metrics=[
            {
                "name": "  Revenue  ",
                "value": "25.2",
                "unit": " billion USD ",
                "evidence": " Revenue was $25.2 billion. ",
            }
        ],
        guidance="   ",
        risks=["  Demand uncertainty  ", " ", "Supply-chain disruption"],
    )

    assert extraction.company == "Tesla"
    assert extraction.reporting_period == "Q2 2025"
    assert extraction.metrics[0].name == "Revenue"
    assert extraction.guidance is None
    assert extraction.risks == ["Demand uncertainty", "Supply-chain disruption"]
