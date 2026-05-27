# Cashflow MVP Backend

A FastAPI backend for the personal cashflow bookkeeping app.

## Setup

```bash
# Install dependencies
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## API Endpoints

- `/api/transactions` - Transaction CRUD
- `/api/assets` - Asset management
- `/api/liabilities` - Liability management
- `/api/reports/balance-sheet` - Balance sheet report
- `/api/reports/monthly-cashflow` - Monthly cashflow report
