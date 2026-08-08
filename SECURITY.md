# Credential and API-Key Safety

## Non-negotiable rules

- Real credentials belong only in ignored local `.env` files or an approved secret manager.
- Source code and practice labs read named environment variables such as `GEMINI_API_KEY` or `OPENROUTER_API_KEY`.
- `.env.example` contains placeholders only.
- Never print, log, screenshot, commit, or paste credential values or prefixes.
- Run `python3 scripts/check_secrets.py` before every commit and push.
- Local pre-commit and pre-push hooks live in `.githooks`; CI runs the same scanner on GitHub.

## Safe Python pattern

```python
import os

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")
```

Do not include the value in an exception or debug statement.

## If a key may have leaked

1. Stop commits, pushes, and application use of the affected key.
2. Revoke or rotate the key at the provider immediately. Deleting it from the latest file is not sufficient.
3. Identify whether it entered Git history, logs, artifacts, screenshots, or chat messages without reproducing the value.
4. Remove the secret from the working tree and, if necessary, rewrite affected Git history.
5. Re-run the repository scanner and verify GitHub/CI before resuming work.

Never treat a secret as safe merely because the repository is private.
