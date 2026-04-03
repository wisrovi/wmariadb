# Test Suite

Unit and integration tests for wmariadb library.

## Structure

```
test/
├── unit/           # Unit tests
│   └── test_basics.py
└── integration/   # Integration tests
```

## Running Tests

```bash
pytest
pytest --cov=wmariadb
pytest --cov=wmariadb --cov-report=html
```