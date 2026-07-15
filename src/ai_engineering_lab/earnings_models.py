from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class FinancialMetric(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    value: Decimal
    unit: str = Field(min_length=1, max_length=50)
    evidence: str = Field(min_length=1)

    @field_validator("name", "unit", "evidence")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class EarningsExtraction(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    reporting_period: str = Field(min_length=1, max_length=100)
    metrics: list[FinancialMetric] = Field(min_length=1)
    guidance: str | None = None
    risks: list[str] = Field(default_factory=list)

    @field_validator("company", "reporting_period")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("guidance")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        return cleaned or None

    @field_validator("risks")
    @classmethod
    def clean_risks(cls, values: list[str]) -> list[str]:
        return [risk.strip() for risk in values if risk.strip()]
