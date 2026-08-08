# Project Learning and Progress Instructions

These instructions apply to every Codex task working anywhere in this repository.

## Read before advising

At the start of a learning, planning, course, or implementation task, read:

1. `docs/session_context.md` - primary current checkpoint and exact next action.
2. `coursera_notes/progress.md` - course and portfolio milestone tracker.
3. `learning_log.md` - completed sessions, concepts, decisions, and failures.
4. `coursera_notes/lab_guidelines.md` - study and assistance rules.

Do not infer progress from an old chat or an outdated handoff when these files disagree. `docs/session_context.md` is authoritative.

## Sequential-work rule

The learner does one focus block at a time and does not combine course study with project implementation in the same block.

Use this pattern:

`complete one course block -> pause the course -> complete its dedicated project sprint -> start the next course block`

Do not propose “learn this while implementing it,” daily course/project alternation, or other parallel workflows unless the learner explicitly changes this preference.

## Automatic progress tracking

After a meaningful milestone, update the relevant files without requiring the learner to remind you:

- Update `coursera_notes/progress.md` when a module, course, or portfolio milestone starts, completes, pauses, or changes order.
- Update `docs/session_context.md` with the exact current focus, verified accomplishments, blockers, and one next action.
- Append a concise dated entry to `learning_log.md` after a substantive study or build session.
- Update `coursera_notes/notes.md` only for durable, job-relevant knowledge that is new or corrected.
- Update `coursera_notes/interview_questions.md` only when a useful interview concept or project story is added or materially improved.

Do not edit tracking files for greetings, minor questions, or unverified intentions. Never mark a course/module complete without learner confirmation or repository evidence.

## PDF synchronization

Markdown is the editable source of truth. When one of these sources changes, regenerate its matching PDF with `scripts/generate_learning_pdfs.py` and visually verify the affected PDF:

- `docs/AI_Application_Engineering_16_Week_Plan.md`
- `coursera_notes/course_1_master_revision.md`
- `coursera_notes/course_2_master_revision.md`
- `coursera_notes/interview_questions.md`

Progress-only changes do not require regenerating unrelated PDFs.

## Mandatory API-key and secret safety

Protect credentials as a hard release gate for every practice lab, generated file, commit, and push.

- Never place an actual API key, token, password, private key, connection string, or credential JSON in source code, tests, notebooks, Markdown, PDFs, sample data, commands, logs, screenshots, or chat responses.
- Never print a secret or even a secret prefix for debugging. Check only whether the required environment variable exists and report the variable name, never its value.
- Do not read or display `.env` contents unless the learner explicitly requests a narrowly scoped operation that cannot be completed safely another way. Prefer metadata-only checks.
- Practice labs must load credentials from environment variables, optionally through `python-dotenv`. Missing-key errors may name the variable but must not include a value.
- Keep real values only in ignored local `.env` files or an approved secret manager. `.env.example` files contain placeholder values only.
- Before every commit and every push, run `python3 scripts/check_secrets.py`. Do not commit or push if it reports any finding.
- Confirm local Git hooks use `.githooks` and that CI retains the secret-scan step.
- If a possible secret is found in tracked content or Git history, stop. Do not push. Tell the learner to revoke/rotate the credential immediately, then remove it from the working tree and history as appropriate.
- A credential pasted by the learner must never be copied into repository files. Recommend rotation if it may have been exposed.

## Dynamic status

Do not keep a second progress snapshot in this instruction file. Always obtain the current course, project block, and next action from `docs/session_context.md`; update that file as progress changes.

## Honesty and preservation

- Distinguish implemented features from course exercises and planned work.
- Preserve existing user changes and session history.
- Record failures and blockers as useful progress evidence.
- Keep notes concise and directly relevant to employability or the current project.
