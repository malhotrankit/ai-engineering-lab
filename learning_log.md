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

