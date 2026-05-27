# Cashflow MVP Backend

FastAPI backend for the cashflow app.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs available at http://localhost:8000/docs

## API Endpoints

### Transactions
- `GET /api/transactions` - List all
- `POST /api/transactions` - Create (auto-classified)
- `GET /api/transactions/{id}` - Get one
- `PUT /api/transactions/{id}` - Update
- `DELETE /api/transactions/{id}` - Delete

Query params: `?month=2024-01`

### Assets
- `GET /api/assets` - List all
- `POST /api/assets` - Create
- `DELETE /api/assets/{id}` - Delete

### Liabilities
- `GET /api/liabilities` - List all
- `POST /api/liabilities` - Create
- `DELETE /api/liabilities/{id}` - Delete

### Reports
- `GET /api/balance-sheet/summary` - Net worth
- `GET /api/cashflow/monthly/{month}` - Monthly cashflow

## Test

```bash
pytest
```

## Project Structure

```
app/
├── main.py           # App entry
├── database.py       # DB config
├── models.py         # SQLModel models
├── schemas.py        # Pydantic schemas
├── classifier.py     # Auto-classification
└── routers/
    ├── transactions.py
    ├── assets.py
    ├── liabilities.py
    ├── balance_sheet.py
    └── cashflow.py
```
