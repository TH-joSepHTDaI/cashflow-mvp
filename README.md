# Cashflow MVP

A minimal personal cashflow bookkeeping app.

## Stack

- **Backend**: FastAPI + SQLite
- **Mobile**: Flutter

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Mobile

```bash
cd mobile/cashflow_mvp
flutter pub get
flutter run
```

## Project Structure

```
cashflow-mvp/
├── backend/          # FastAPI backend
│   ├── app/          # Application code
│   └── tests/        # Test suite
├── mobile/           # Flutter app
│   └── cashflow_mvp/
└── docs/             # Documentation
```

## Features

- Transaction tracking (income, expense, investment, liability repayment)
- Auto-classification based on keywords
- Asset management
- Liability management
- Balance sheet (net worth calculation)
- Monthly cashflow analysis

## API Endpoints

- `GET/POST /api/transactions` - Transactions
- `GET/POST /api/assets` - Assets
- `GET/POST /api/liabilities` - Liabilities
- `GET /api/balance-sheet` - Balance sheet
- `GET /api/cashflow/monthly/{month}` - Cashflow

See [backend/README.md](backend/README.md) for details.

## Testing

```bash
cd backend
pytest
```

67 tests passing.

## License

MIT
