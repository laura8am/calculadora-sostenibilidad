# Test Suite for Calculadora de Sostenibilidad

This directory contains comprehensive unit tests for the sustainability calculator application.

## Test Coverage

The test suite covers three core functions with **68 test cases**:

### 1. `normalizar_inverso()` - 14 tests
- Normal value normalization
- Edge cases (min, max, equal values)
- Real dataset ranges (Carbon Footprint, Water Footprint, NOVA)
- Extrapolation scenarios
- Negative value ranges

### 2. `calcular_score_producto()` - 21 tests
- Perfect and worst product scenarios (A & B)
- Weight validation (ensure they sum to 1.0)
- Mid-range value calculations
- Manual calculation verification
- Scenario A vs B comparisons
- Waste indicator impact analysis
- Return value structure validation
- Edge cases (zero values, out-of-range)

### 3. `clasificar_score()` - 29 tests
- All category boundaries (Excelente, Muy Bueno, Bueno, Moderado, Bajo)
- Boundary transitions (89.99 vs 90, etc.)
- Edge cases (negative scores, >100)
- Return value structure
- Emoji validation for all categories

### 4. Integration Tests - 4 tests
- Full workflow for excellent and poor products
- Cross-scenario comparisons
- Normalized value impact verification

## Running the Tests

### Prerequisites

Install the required testing dependencies:

```bash
pip install -r requirements_v2.txt
```

This will install pytest along with all other project dependencies.

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test Classes

```bash
# Test only normalization function
pytest test_app_calculadora_sostenibilidad_v2.py::TestNormalizarInverso

# Test only score calculation
pytest test_app_calculadora_sostenibilidad_v2.py::TestCalcularScoreProducto

# Test only classification
pytest test_app_calculadora_sostenibilidad_v2.py::TestClasificarScore

# Test only integration scenarios
pytest test_app_calculadora_sostenibilidad_v2.py::TestIntegrationScenarios
```

### Run Specific Test Methods

```bash
# Test a specific scenario
pytest test_app_calculadora_sostenibilidad_v2.py::TestCalcularScoreProducto::test_escenario_a_perfect_product
```

### Generate Coverage Report

```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest --cov=app_calculadora_sostenibilidad_v2 --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Structure

```
test_app_calculadora_sostenibilidad_v2.py
├── TestNormalizarInverso          (14 tests)
├── TestCalcularScoreProducto      (21 tests)
├── TestClasificarScore            (29 tests)
└── TestIntegrationScenarios       (4 tests)
```

## Key Test Scenarios

### Normalization Tests
- Verifies inverse normalization (lower values = better scores)
- Tests special case where min == max (returns 50)
- Validates actual dataset ranges

### Score Calculation Tests
- **Scenario A**: Waste weight = 25%
- **Scenario B**: Waste weight = 30%
- Verifies all weights sum to 1.0
- Tests that changing waste value affects score by expected amount

### Classification Tests
- **Excelente**: score >= 90 (🟢)
- **Muy Bueno**: 80 <= score < 90 (🟢)
- **Bueno**: 70 <= score < 80 (🟡)
- **Moderado**: 60 <= score < 70 (🟠)
- **Bajo**: score < 60 (🔴)

## Expected Results

All 68 tests should pass:

```
====== 68 passed in 0.XX s ======
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines using GitHub Actions, GitLab CI, or similar tools.

Example GitHub Actions workflow:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements_v2.txt
      - name: Run tests
        run: pytest -v
```

## Contributing

When adding new features to the calculator:
1. Write tests first (TDD approach)
2. Ensure all existing tests still pass
3. Add new test cases for edge cases
4. Maintain test coverage above 80%

## Notes

- Tests use `pytest.approx()` for floating-point comparisons
- Tests are independent and can run in any order
- No external data files required (all test data is inline)
- Tests run in < 1 second
