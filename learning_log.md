# Week 0–1 — Production Python Baseline

## Why use a virtual environment?

A virtual environment creates an isolated set of Python packages for one project.
It prevents package versions from different projects from conflicting with each
other. It also makes the project reproducible because the needed dependencies
can be installed separately for this project.

## Parsing versus validation

Parsing means reading input and converting it into a usable Python value or
object. For example, JSON from an API can be parsed into Python data.

Validation checks whether that data follows the application's rules. For the
Document model, validation ensures that title and content are meaningful, the
page number is at least 1, and a supplied source URL uses HTTP or HTTPS.

## Why is a Pydantic model useful in an AI application?

AI applications receive data from sources that cannot be fully trusted, such as
user requests, PDF parsers, APIs, databases, and LLM responses. A Pydantic model
defines the expected structure and validates the data before the rest of the
application uses it. This catches invalid or incomplete data early.

## Unit test versus integration test

A unit test checks one small part of the system in isolation. For example, a
unit test can check that the Document model rejects a page number of 0.

An integration test checks whether multiple components work together. Later, an
integration test could check whether a FastAPI endpoint receives a document,
validates it with Pydantic, and stores it in a database.

## One failure case my Document model prevents

The Document model prevents invalid document data such as a whitespace-only
title, an empty content field, a page number of 0, or a malformed source URL.
Rejecting these values early stops bad data from entering later RAG or AI
processing steps.


## Session 2 — Date: 2026-07-12

### Completed

- Reviewed the full Pydantic `Document` model
- Understood its fields: title, content, page number, optional source URL, and metadata
- Understood custom validators for whitespace-only text and HTTP/HTTPS URLs
- Added `test_document_trims_title_and_content`
- Ran the test suite successfully: 6 tests passed
- Checked Ruff formatting successfully

### Concepts understood

- A URL is optional because documents can originate from local uploads or internal systems
- `default_factory=dict` creates a separate empty metadata dictionary for every Document object
- `Field(min_length=1)` checks string length; the custom validator trims whitespace and rejects text that has no meaningful characters

### Files changed

- `tests/test_models.py`
- `learning_log.md`
- `docs/session_context.md`

### Next step

Set up Git configuration if needed, create the first Git commit, then add GitHub Actions so tests and Ruff checks run automatically on every push.


## Session 2 Answers to Conceptual Questions

1. **Why must every extracted metric include an `evidence` field?**
The evidence field provides the exact source text from which the data was fetched, allowing us to verify the LLM's claim and ensure it isn't hallucinated.

2. **Why does a metric need both `value` and `unit`?**
A raw number isn't enough; the unit specifies whether the value is in millions, billions, percentages, or another currency, giving it necessary context.

3. **Why is `metrics` a list rather than a single `FinancialMetric`?**
Earnings reports contain multiple financial metrics (like Revenue, EPS, Gross Margin), not just one, so we need a list to capture all of them.

4. **Why may `guidance` be `None`, while `company` may not?**
Not all companies provide future guidance in every report, making it optional, whereas the company name is a fundamental requirement for the extraction to be valid.

## Session 4 — Date: 2026-07-17

### Completed
- Configured `.env` file securely and installed `google-genai` and `python-dotenv`.
- Built `live_extractor.py` to call the Gemini API using the new structured outputs feature.
- Passed our Pydantic `EarningsExtraction` schema directly into the `response_schema` config to force the LLM to return perfectly structured data.
- Tested the live API successfully against a sample Apple earnings report.

### Concepts understood
- **API Security:** API keys must be kept in `.env` files and ignored by Git to prevent massive accidental billing charges from leaked credentials.
- **Structured Outputs via API:** We can force modern LLMs to conform to Pydantic schemas natively through the API configuration, ensuring we get a clean object without manual string parsing.
- **The Grounding Reality:** Even with the live API enforcing the schema perfectly, the LLM can still hallucinate numbers that fit the structure. The deterministic `verify_evidence` function we wrote earlier remains mandatory to prove factual grounding!
- **Hallucinated Evidence:** The LLM can easily hallucinate the `evidence` string itself. Pydantic will accept the hallucinated string because it's technically a valid string. Our deterministic `verify_evidence` function is the only way to prove the LLM's quoted evidence actually exists in the original raw text.



## Session 3 — Date: 2026-07-16

### Completed

- Implemented a clean, simple, keyword-based `extract_earnings_fake` and `verify_evidence` in [fake_extractor.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/src/ai_engineering_lab/fake_extractor.py).
- Created unit tests in [test_fake_extractor.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/tests/test_fake_extractor.py) to cover:
  - Valid structured outputs that pass Pydantic validation and grounding checks.
  - Malformed structured outputs that fail Pydantic validation.
  - Ungrounded structured outputs that pass Pydantic validation but fail grounding checks.
- Formatted and linted files with Ruff.
- Ran test suite successfully (15 tests passed).

### Session 3 Answers to Conceptual Questions

1. **Why can Pydantic accept a fabricated claim?**
   Pydantic validates the data structure, field types, and constraints (e.g. string length, non-empty fields). It does not check if the content of the data matches the reality of the source text.

2. **What does a schema prove, and what does it not prove?**
   A schema proves structural conformity and type correctness (e.g., this is a list of financial metrics with required fields). It does not prove that the data is true, grounded in the source document, or mathematically correct.

3. **Why is an evidence quote useful but not automatically enough?**
   An evidence quote allows verification (so humans or automated systems can verify the claim against the source document). It is not enough on its own because the model might have fabricated the quote itself (hallucination) or selected a quote that doesn't actually support the extracted value.

4. **Why must financial calculations remain deterministic Python code rather than LLM arithmetic?**
   LLMs are next-token predictors and lack a reliable mathematical reasoning engine. They often make arithmetic errors, whereas deterministic Python code using exact precision types (like `Decimal`) guarantees 100% mathematical accuracy and reproducibility.

