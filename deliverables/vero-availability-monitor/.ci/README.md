# CI

Plan `QAI-vero-availability-monitor-PRGATE`: ruff check, mypy (strict), unit + integration tests, secret scan.

```
uvx ruff check .
uvx mypy
python -m unittest discover -s tests -t .
```
