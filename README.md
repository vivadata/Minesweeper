# Minesweeper

## Run tests

```bash
make tests
```

## Run tests with coverage

```bash
make coverage
```

This command generates:
- a terminal coverage summary with missing lines
- `coverage.xml` (useful for CI integrations)

Coverage is configured in `.coveragerc` and focuses on `web/` and `src/` code.
