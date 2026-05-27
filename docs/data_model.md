# 🗄️ 数据模型文档

本文档描述 Cashflow MVP 的数据库设计和模型关系。

---

## 概述

- **数据库**: SQLite
- **ORM**: SQLModel (基于 SQLAlchemy 2.0)
- **设计原则**: 简单、直观、易于扩展

---

## 实体关系图 (ERD)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Transaction   │     │     Asset       │     │   Liability     │
│    (交易记录)    │     │    (资产)        │     │    (负债)        │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ PK id           │     │ PK id           │     │ PK id           │
│    amount       │     │    name         │     │    name         │
│    date         │     │    asset_type   │     │    liability_type│
│    note         │     │    value        │     │    value        │
│    category     │     │    created_at   │     │    created_at   │
│    cashflow_type│     │    updated_at   │     │    updated_at   │
│    created_at   │     └─────────────────┘     └─────────────────┘
│    updated_at   │
└─────────────────┘
```

**说明：** 三个实体相互独立，没有外键关联（MVP 设计简化）

---

## 详细模型定义

### 1. Transaction (交易记录)

存储每一笔收入、支出、投资或负债还款。

**表名**: `transactions`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| amount | FLOAT | 是 | 金额（正数） |
| date | VARCHAR | 是 | 交易日期，格式 `YYYY-MM-DD` |
| note | VARCHAR | 否 | 备注/描述 |
| category | VARCHAR | 是 | 分类（如：food, salary） |
| cashflow_type | VARCHAR | 是 | 现金流类型（见下方枚举） |
| created_at | DATETIME | 是 | 创建时间 |
| updated_at | DATETIME | 是 | 更新时间 |

**cashflow_type 枚举值：**

| 值 | 中文 | 说明 |
|----|------|------|
| `income` | 收入 | 工资、奖金、投资收益等 |
| `expense` | 支出 | 日常消费、账单等 |
| `investment` | 投资 | 购买股票、基金等 |
| `liability_repayment` | 负债还款 | 还信用卡、贷款等 |
| `other` | 其他 | 未分类 |

**示例数据：**

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

### 2. Asset (资产)

存储用户的各类资产及其当前价值。

**表名**: `assets`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| name | VARCHAR | 是 | 资产名称 |
| asset_type | VARCHAR | 是 | 资产类型（见下方枚举） |
| value | FLOAT | 是 | 当前价值 |
| created_at | DATETIME | 是 | 创建时间 |
| updated_at | DATETIME | 是 | 更新时间 |

**asset_type 枚举值：**

| 值 | 中文 | 示例 |
|----|------|------|
| `cash` | 现金 | 钱包现金、备用金 |
| `bank_deposit` | 银行存款 | 活期、定期存款 |
| `fund_etf_stock` | 基金/股票 | 股票账户、基金投资 |
| `property` | 房产 | 自住房、投资房 |
| `other` | 其他 | 车辆、珠宝等 |

**示例数据：**

```json
{
  "id": 1,
  "name": "Emergency Fund",
  "asset_type": "bank_deposit",
  "value": 50000.00,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 3. Liability (负债)

存储用户的各类负债及其当前余额。

**表名**: `liabilities`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| name | VARCHAR | 是 | 负债名称 |
| liability_type | VARCHAR | 是 | 负债类型（见下方枚举） |
| value | FLOAT | 是 | 当前余额（正数表示欠款） |
| created_at | DATETIME | 是 | 创建时间 |
| updated_at | DATETIME | 是 | 更新时间 |

**liability_type 枚举值：**

| 值 | 中文 | 示例 |
|----|------|------|
| `credit_card` | 信用卡 | 信用卡账单 |
| `mortgage` | 房贷 | 房屋抵押贷款 |
| `car_loan` | 车贷 | 车辆贷款 |
| `consumer_loan` | 消费贷 | 个人消费贷款 |
| `other` | 其他 | 其他借款 |

**示例数据：**

```json
{
  "id": 1,
  "name": "Visa Credit Card",
  "liability_type": "credit_card",
  "value": 5000.00,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## 计算逻辑

### 净资产计算

```
净资产 = 总资产 - 总负债

其中：
- 总资产 = SUM(Asset.value)
- 总负债 = SUM(Liability.value)
```

### 月度现金流计算

```
净现金流 = 收入 - 支出 - 投资 - 负债还款

其中：
- 收入 = SUM(Transaction.amount WHERE cashflow_type = 'income')
- 支出 = SUM(Transaction.amount WHERE cashflow_type = 'expense')
- 投资 = SUM(Transaction.amount WHERE cashflow_type = 'investment')
- 负债还款 = SUM(Transaction.amount WHERE cashflow_type = 'liability_repayment')
```

---

## 数据库配置

### 文件位置

```python
# backend/app/database.py
DATABASE_PATH = Path(__file__).parent.parent / "data" / "cashflow.db"
```

默认位置：`backend/data/cashflow.db`

### 连接字符串

```
sqlite:///backend/data/cashflow.db
```

### 初始化

首次启动时自动创建表：

```python
# backend/app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # 创建表
    yield
```

---

## 数据备份

### 手动备份

```bash
# 复制数据库文件
cp backend/data/cashflow.db backup/cashflow_$(date +%Y%m%d).db
```

### 自动备份（建议）

```bash
# 添加到 crontab，每天凌晨备份
0 0 * * * cp /path/to/cashflow.db /path/to/backup/cashflow_$(date +\%Y\%m\%d).db
```

---

## 扩展设计（未来版本）

### 可能的扩展

1. **User 表** - 支持多用户
   ```
   User
   ├── id
   ├── username
   ├── email
   ├── password_hash
   └── created_at
   ```

2. **Budget 表** - 预算设置
   ```
   Budget
   ├── id
   ├── user_id (FK)
   ├── category
   ├── amount
   └── month
   ```

3. **Account 表** - 多账户支持
   ```
   Account
   ├── id
   ├── user_id (FK)
   ├── name
   ├── type
   └── balance
   ```

---

## SQL 示例查询

### 查看所有交易

```sql
SELECT * FROM transactions ORDER BY date DESC;
```

### 按月统计收支

```sql
SELECT 
  strftime('%Y-%m', date) as month,
  cashflow_type,
  SUM(amount) as total
FROM transactions
GROUP BY month, cashflow_type;
```

### 计算净资产

```sql
SELECT 
  (SELECT SUM(value) FROM assets) as total_assets,
  (SELECT SUM(value) FROM liabilities) as total_liabilities,
  (SELECT SUM(value) FROM assets) - (SELECT SUM(value) FROM liabilities) as net_worth;
```
