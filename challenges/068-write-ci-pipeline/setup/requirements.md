# CI/CD Pipeline Requirements

## Workflow Name
`CI/CD Pipeline`

## Triggers
- Push to `main` branch
- Pull requests targeting `main` branch

## Jobs

### 1. Test Job (`test`)

**Runner**: `ubuntu-latest`

**Strategy**: Build matrix with Python versions `3.10`, `3.11`, and `3.12`

**Steps**:
1. **Checkout** code using `actions/checkout`
2. **Set up Python** using `actions/setup-python` with the matrix Python version
3. **Cache pip dependencies** using `actions/cache` with:
   - Path: `~/.cache/pip`
   - Key based on runner OS and `requirements.txt` hash
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run tests**: `pytest tests/ -v --cov=src --cov-report=xml`
6. **Upload coverage artifact** using `actions/upload-artifact` with:
   - Name: `coverage-report-${{ matrix.python-version }}`
   - Path: `coverage.xml`

### 2. Deploy Job (`deploy`)

**Runner**: `ubuntu-latest`

**Needs**: `test` (must pass first)

**Condition**: Only run on push to the `main` branch (not on pull requests)

**Steps**:
1. **Checkout** code using `actions/checkout`
2. **Set up Python** using `actions/setup-python` with Python `3.12`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Deploy**: `python deploy.py --env production`
