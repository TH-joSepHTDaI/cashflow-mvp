# 🔌 API 规范文档

本文档详细描述 Cashflow MVP 的所有 API 端点。

---

## 基础信息

- **基础 URL**: `http://localhost:8000`
- **API 前缀**: `/api`
- **内容类型**: `application/json`
- **文档地址**: http://localhost:8000/docs (Swagger UI)

---

## 通用响应格式

### 成功响应

```json
{
  "id": 1,
  "amount": 100.50,
  "date": "2024-01-15",
  "category": "food",
  "cashflow_type": "expense"
}
```

### 错误响应

```json
{
  "detail": "Transaction not found"
}
```

### HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容）|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 验证错误 |

---

## 交易 API

### 列出交易

```http
GET /api/transactions/
```

**查询参数：**
- `month` (可选): 格式 `YYYY-MM`，如 `2024-01`

**响应示例：**
```json
[
  {
    "id": 1,
    "amount": 5000.00,
    "date": "2024-01-15",
    "note": "Monthly salary",
    "category": "salary",
    "cashflow_type": "income",
    "created_at": "2024-01-15T08:00:00",
    "updated_at": "2024-01-15T08:00:00"
  }
]
```

---

### 创建交易

```http
POST /api/transactions/
```

**请求体：**
```json
{
  "amount": 100.50,
  "date": "2024-01-15",
  "note": "Lunch at restaurant",
  "category": "food"
}
```

**说明：**
- 如果不提供 `cashflow_type`，系统会根据 `note` 和 `category` 自动分类
- 例如：包含"工资"→收入，"午餐"→支出

**响应示例：**
```json
{
  "id": 2,
  "amount": 100.50,
  "date": "2024-01-15",
  "note": "Lunch at restaurant",
  "category": "food",
  "cashflow_type": "expense",
  "created_at": "2024-01-15T12:30:00",
  "updated_at": "2024-01-15T12:30:00"
}
```

---

### 获取单个交易

```http
GET /api/transactions/{transaction_id}
```

**响应示例：**
```json
{
  "id": 1,
  "amount": 5000.00,
  "date": "2024-01-15",
  "note": "Monthly salary",
  "category": "salary",
  "cashflow_type": "income",
  "created_at": "2024-01-15T08:00:00",
  "updated_at": "2024-01-15T08:00:00"
}
```

---

### 更新交易

```http
PUT /api/transactions/{transaction_id}
```

**请求体：**（所有字段可选）
```json
{
  "amount": 150.00,
  "note": "Updated note"
}
```

---

### 删除交易

```http
DELETE /api/transactions/{transaction_id}
```

**响应：** 204 No Content

---

## 资产 API

### 列出资产

```http
GET /api/assets/
```

**响应示例：**
```json
[
  {
    "id": 1,
    "name": "Savings Account",
    "asset_type": "bank_deposit",
    "value": 50000.00,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

---

### 创建资产

```http
POST /api/assets/
```

**请求体：**
```json
{
  "name": "Stock Portfolio",
  "asset_type": "fund_etf_stock",
  "value": 100000.00
}
```

**资产类型：**
- `cash` - 现金
- `bank_deposit` - 银行存款
- `fund_etf_stock` - 基金/股票
- `property` - 房产
- `other` - 其他

---

### 删除资产

```http
DELETE /api/assets/{asset_id}
```

---

## 负债 API

### 列出负债

```http
GET /api/liabilities/
```

**响应示例：**
```json
[
  {
    "id": 1,
    "name": "Credit Card",
    "liability_type": "credit_card",
    "value": 5000.00,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

---

### 创建负债

```http
POST /api/liabilities/
```

**请求体：**
```json
{
  "name": "Home Mortgage",
  "liability_type": "mortgage",
  "value": 500000.00
}
```

**负债类型：**
- `credit_card` - 信用卡
- `mortgage` - 房贷
- `car_loan` - 车贷
- `consumer_loan` - 消费贷
- `other` - 其他

---

### 删除负债

```http
DELETE /api/liabilities/{liability_id}
```

---

## 资产负债表 API

### 简要汇总

```http
GET /api/balance-sheet/summary
```

**响应示例：**
```json
{
  "total_assets": 150000.00,
  "total_liabilities": 50000.00,
  "net_worth": 100000.00,
  "asset_count": 3,
  "liability_count": 1,
  "generated_at": "2024-01-15T10:00:00"
}
```

---

### 完整资产负债表

```http
GET /api/balance-sheet/
```

**响应示例：**
```json
{
  "summary": {
    "total_assets": 150000.00,
    "total_liabilities": 50000.00,
    "net_worth": 100000.00
  },
  "assets": {
    "total": 150000.00,
    "by_type": {
      "bank_deposit": 50000.00,
      "fund_etf_stock": 100000.00
    },
    "items": [
      {
        "id": 1,
        "name": "Savings Account",
        "type": "bank_deposit",
        "value": 50000.00
      }
    ]
  },
  "liabilities": {
    "total": 50000.00,
    "by_type": {
      "credit_card": 5000.00,
      "mortgage": 45000.00
    },
    "items": [
      {
        "id": 1,
        "name": "Credit Card",
        "type": "credit_card",
        "value": 5000.00
      }
    ]
  },
  "generated_at": "2024-01-15T10:00:00"
}
```

---

## 现金流 API

### 单月现金流

```http
GET /api/cashflow/monthly/{year_month}
```

**路径参数：**
- `year_month`: 格式 `YYYY-MM`，如 `2024-01`

**响应示例：**
```json
{
  "month": "2024-01",
  "summary": {
    "total_income": 10000.00,
    "total_expense": 3000.00,
    "total_investment": 2000.00,
    "total_liability_repayment": 1000.00,
    "net_cashflow": 4000.00,
    "transaction_count": 15
  },
  "details": {
    "income": {
      "total": 10000.00,
      "count": 1,
      "items": [...]
    },
    "expense": {
      "total": 3000.00,
      "count": 8,
      "items": [...]
    },
    "investment": {
      "total": 2000.00,
      "count": 2,
      "items": [...]
    },
    "liability_repayment": {
      "total": 1000.00,
      "count": 4,
      "items": [...]
    }
  },
  "generated_at": "2024-01-15T10:00:00"
}
```

---

### 现金流汇总

```http
GET /api/cashflow/summary?month=2024-01
```

**查询参数：**
- `month` (可选): 格式 `YYYY-MM`，默认当前月

**响应示例：**
```json
{
  "month": "2024-01",
  "total_income": 10000.00,
  "total_expense": 3000.00,
  "total_investment": 2000.00,
  "total_liability_repayment": 1000.00,
  "net_cashflow": 4000.00,
  "transaction_count": 15,
  "generated_at": "2024-01-15T10:00:00"
}
```

---

### 按分类统计

```http
GET /api/cashflow/by-category/2024-01
```

**响应示例：**
```json
{
  "month": "2024-01",
  "categories": [
    {
      "category": "salary",
      "income": 10000.00,
      "expense": 0.00,
      "investment": 0.00,
      "liability_repayment": 0.00,
      "net": 10000.00
    },
    {
      "category": "food",
      "income": 0.00,
      "expense": 1500.00,
      "investment": 0.00,
      "liability_repayment": 0.00,
      "net": -1500.00
    }
  ],
  "generated_at": "2024-01-15T10:00:00"
}
```

---

## 健康检查

```http
GET /health
```

**响应示例：**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 快速测试命令

```bash
# 测试健康检查
curl http://localhost:8000/health

# 创建交易
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "date": "2024-01-15", "category": "food", "note": "lunch"}'

# 列出交易
curl http://localhost:8000/api/transactions/

# 查看资产负债表
curl http://localhost:8000/api/balance-sheet/summary
```
