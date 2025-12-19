# Test Suite

## Overview

This test suite validates Präsens conjugation correctness for German verbs.

## Running Tests

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_präsens.py

# Run a specific test
pytest tests/test_präsens.py::test_essen_du
```

## Test Coverage

The test suite covers:

1. **Stem-change verbs** (e.g., essen → isst, lesen → liest)
2. **Epenthetic -e- verbs** (e.g., warten → wartest, arbeiten → arbeitet)
3. **Separable verbs** (e.g., aufstehen → steht)
4. **Reflexive verbs** (e.g., sich freuen → freust)
5. **Combined cases** (reflexive + separable, e.g., sich anziehen → zieht)
6. **Regular verbs** (sanity checks)
7. **Modal verbs** (special cases)

## Principles

- **Deterministic**: Tests always produce the same results
- **Explicit**: Each test asserts a concrete expected string
- **No randomness**: All inputs and outputs are fixed
- **Core-only**: Tests only the grammar engine, no UI/CLI dependencies

