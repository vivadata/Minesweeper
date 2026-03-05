# Minesweeper

## Quick start

Prerequisites:
- `pyenv`
- `pyenv-virtualenv`

Install dependencies:

```bash
make install
```

Run the app:

```bash
make app
```

## Tests

Run all tests:

```bash
make tests
```

Run test subsets:

```bash
make unit-tests
make functional-tests
```

## Coverage

Generate coverage reports:

```bash
make coverage
```

Outputs:
- terminal summary (`term-missing`)
- `tests_result/coverage.xml`
- `tests_result/junit.xml`
- `tests_result/htmlcov/index.html`

Coverage scope is configured in `.coveragerc` for `src/` and `web/`.
