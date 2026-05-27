# API Specification

Base URL: `http://localhost:8000`

## Transactions

### List
```
GET /api/transactions
GET /api/transactions?month=2024-01
```

### Create
```
POST /api/transactions
{
  "amount": 100.00,
  "date": "2024-01-15",
  "category": "food",
  "note": "lunch"
}
```
Auto-classified based on keywords.

### Get/Update/Delete
```
GET    /api/transactions/{id}
PUT    /api/transactions/{id}
DELETE /api/transactions/{id}
```

## Assets

```
GET    /api/assets
POST   /api/assets
DELETE /api/assets/{id}
```

## Liabilities

```
GET    /api/liabilities
POST   /api/liabilities
DELETE /api/liabilities/{id}
```

## Reports

### Balance Sheet
```
GET /api/balance-sheet/summary
```

### Cashflow
```
GET /api/cashflow/monthly/{year-month}
GET /api/cashflow/summary?month=2024-01
```
