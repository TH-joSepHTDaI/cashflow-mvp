# Test Plan

## Backend Tests

Run: `pytest`

### Test Files

| File | Tests |
|------|-------|
| test_main.py | Health check |
| test_database.py | DB connection |
| test_classifier.py | Auto-classification |
| test_transactions.py | Transaction CRUD |
| test_assets.py | Asset CRUD |
| test_liabilities.py | Liability CRUD |
| test_balance_sheet.py | Balance sheet |
| test_cashflow.py | Cashflow reports |

**Total: 67 tests**

## Coverage

```bash
pytest --cov=app
```

Current: ~99%
