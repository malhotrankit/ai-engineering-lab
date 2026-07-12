import pytest
from pydantic import ValidationError

from ai_engineering_lab.models import Document


def test_document_accepts_valid_data() -> None:
    document = Document(
        title="Example annual report",
        content="Revenue increased during the reporting period.",
        page_number=12,
        source_url="https://example.com/report.pdf",
        metadata={"company": "Example Corp", "fiscal_year": 2025},
    )

    assert document.page_number == 12
    assert document.metadata["company"] == "Example Corp"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", "   "),
        ("content", ""),
        ("page_number", 0),
        ("source_url", "example.com/report.pdf"),
    ],
)
def test_document_rejects_invalid_data(field: str, value: object) -> None:
    valid_data = {
        "title": "Example annual report",
        "content": "Revenue increased during the reporting period.",
        "page_number": 12,
        "source_url": "https://example.com/report.pdf",
    }
    valid_data[field] = value

    with pytest.raises(ValidationError):
        Document(**valid_data)


def test_document_trims_title_and_content() -> None:
    document = Document(
        title="  Example annual report  ",
        content="  Revenue increased.  ",
        page_number=12,
    )

    assert document.title == "Example annual report"
    assert document.content == "Revenue increased."
