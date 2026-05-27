# Data Model

## Tables

### transactions

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| amount | FLOAT | Transaction amount |
| date | VARCHAR | YYYY-MM-DD |
| note | VARCHAR | Optional description |
| category | VARCHAR | Category name |
| cashflow_type | VARCHAR | income/expense/investment/liability_repayment/other |
| created_at | DATETIME | Auto-generated |
| updated_at | DATETIME | Auto-generated |

### assets

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR | Asset name |
| asset_type | VARCHAR | cash/bank_deposit/fund_etf_stock/property/other |
| value | FLOAT | Current value |
| created_at | DATETIME | Auto-generated |
| updated_at | DATETIME | Auto-generated |

### liabilities

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR | Liability name |
| liability_type | VARCHAR | credit_card/mortgage/car_loan/consumer_loan/other |
| value | FLOAT | Current balance |
| created_at | DATETIME | Auto-generated |
| updated_at | DATETIME | Auto-generated |

## Calculations

- Net worth = SUM(assets.value) - SUM(liabilities.value)
- Monthly cashflow = income - expense - investment - liability_repayment
