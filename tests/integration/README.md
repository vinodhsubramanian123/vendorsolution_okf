# Manual verification scripts

Files here are `def main()` scripts (not pytest tests, despite the old
`test_*.py` naming that used to live here -- pytest silently collected 0
tests from them, which looked like passing integration coverage but
wasn't). Run them directly, e.g.:

```bash
uv run python tests/integration/manual_test_real_boq.py
```

They require `repository/` to already be seeded (`./scripts/bootstrap.sh`)
and are not run by CI or `pytest tests/`.
