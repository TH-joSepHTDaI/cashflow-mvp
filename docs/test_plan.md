# 🧪 测试计划文档

本文档描述 Cashflow MVP 的测试策略和测试用例。

---

## 测试概述

### 测试目标
- 确保所有 API 功能正常工作
- 验证数据一致性
- 保证代码质量

### 测试类型
- **单元测试** - 测试单个函数/组件
- **集成测试** - 测试 API 端点
- **端到端测试** - 测试完整流程（未来版本）

---

## 后端测试

### 测试框架
- **pytest** - 测试框架
- **TestClient** - FastAPI 提供的 HTTP 测试客户端

### 运行测试

```bash
cd backend
source .venv/bin/activate

# 运行所有测试
pytest

# 详细输出
pytest -v

# 运行特定测试文件
pytest tests/test_transactions.py -v

# 查看覆盖率
pytest --cov=app --cov-report=html
```

### 测试文件说明

| 文件 | 测试内容 | 测试数量 |
|------|---------|---------|
| `test_main.py` | 应用启动和健康检查 | 2 |
| `test_database.py` | 数据库连接和模型 | 5 |
| `test_classifier.py` | 交易自动分类 | 14 |
| `test_transactions.py` | 交易 CRUD API | 10 |
| `test_assets.py` | 资产 API | 11 |
| `test_liabilities.py` | 负债 API | 10 |
| `test_balance_sheet.py` | 资产负债表 API | 9 |
| `test_cashflow.py` | 现金流 API | 9 |
| **总计** | | **67** |

---

## 测试用例详情

### 1. 交易分类测试 (test_classifier.py)

**测试目标：** 验证自动分类规则

| 测试用例 | 输入 | 期望输出 |
|---------|------|---------|
| salary_classified_as_income | "Monthly salary" | income |
| rent_classified_as_expense | "Pay rent" | expense |
| food_classified_as_expense | "Restaurant dinner" | expense |
| investment_classified_as_investment | "Buy stock" | investment |
| loan_classified_as_liability | "Credit card payment" | liability_repayment |
| unknown_classified_as_other | "Random text" | other |

**示例代码：**
```python
def test_salary_classified_as_income():
    assert classify_transaction("Monthly salary") == CashflowType.INCOME
```

---

### 2. 交易 API 测试 (test_transactions.py)

**测试目标：** 验证交易 CRUD 操作

| 测试用例 | 方法 | 端点 | 期望结果 |
|---------|------|------|---------|
| test_create_transaction | POST | /api/transactions/ | 201 Created |
| test_list_transactions | GET | /api/transactions/ | 200 OK + 列表 |
| test_list_by_month | GET | /api/transactions/?month=2024-01 | 过滤结果 |
| test_get_transaction | GET | /api/transactions/1 | 200 OK + 详情 |
| test_get_not_found | GET | /api/transactions/999 | 404 Not Found |
| test_update_transaction | PUT | /api/transactions/1 | 200 OK + 更新 |
| test_delete_transaction | DELETE | /api/transactions/1 | 204 No Content |

---

### 3. 资产 API 测试 (test_assets.py)

**测试目标：** 验证资产 CRUD 操作

| 测试用例 | 说明 |
|---------|------|
| test_create_asset | 创建资产成功 |
| test_create_with_different_types | 支持所有资产类型 |
| test_list_assets | 列出所有资产 |
| test_get_asset | 获取单个资产 |
| test_update_asset | 更新资产信息 |
| test_delete_asset | 删除资产 |
| test_value_can_be_zero | 允许资产价值为 0 |
| test_value_can_be_negative | 允许资产价值为负（亏损） |

---

### 4. 负债 API 测试 (test_liabilities.py)

与资产测试类似，验证负债的 CRUD 操作。

---

### 5. 资产负债表测试 (test_balance_sheet.py)

**测试目标：** 验证财务报表计算

| 测试用例 | 说明 |
|---------|------|
| test_balance_sheet_empty | 空数据时返回 0 |
| test_balance_sheet_with_data | 正确计算净资产 |
| test_negative_net_worth | 负债大于资产时显示负数 |
| test_assets_by_type | 按类型筛选资产 |
| test_liabilities_by_type | 按类型筛选负债 |

---

### 6. 现金流测试 (test_cashflow.py)

**测试目标：** 验证现金流统计

| 测试用例 | 说明 |
|---------|------|
| test_monthly_cashflow | 单月现金流统计 |
| test_cashflow_range | 多月范围统计 |
| test_cashflow_by_category | 按分类统计 |
| test_negative_net | 支出大于收入时显示负数 |

---

## 测试覆盖率

当前覆盖率报告：

```
Name                          Stmts   Miss  Cover
-----------------------------------------------
app/__init__.py                   0      0   100%
app/classifier.py                21      0   100%
app/database.py                  14      2    86%
app/main.py                      19      0   100%
app/models.py                    36      0   100%
app/routers/assets.py            33      0   100%
app/routers/balance_sheet.py     56      0   100%
app/routers/cashflow.py          93      0   100%
app/routers/liabilities.py       33      0   100%
app/routers/transactions.py      39      0   100%
app/schemas.py                   36      0   100%
-----------------------------------------------
TOTAL                           380      2    99%
```

---

## 移动端测试（Flutter）

### 测试框架
- **flutter_test** - Flutter 官方测试框架

### 运行测试

```bash
cd mobile/cashflow_mvp

# 运行所有测试
flutter test

# 运行特定测试文件
flutter test test/widget_test.dart
```

### 测试计划

由于 MVP 版本时间限制，移动端测试将在后续版本完善：

- [ ] Widget 测试 - 测试 UI 组件
- [ ] Integration 测试 - 测试完整用户流程
- [ ] Mock API 测试 - 不依赖后端服务的测试

---

## 手动测试清单

在发布前，建议进行以下手动测试：

### 功能测试

- [ ] 创建收入交易
- [ ] 创建支出交易
- [ ] 创建投资交易
- [ ] 创建负债还款交易
- [ ] 验证自动分类
- [ ] 添加资产
- [ ] 添加负债
- [ ] 查看资产负债表
- [ ] 查看月度现金流

### 边界测试

- [ ] 金额为 0 的交易
- [ ] 很长的备注文字
- [ ] 特殊字符的分类名称
- [ ] 跨月日期选择

### 性能测试

- [ ] 100+ 条交易记录的加载速度
- [ ] 大量资产/负债时的资产负债表计算

---

## 持续集成（建议）

### GitHub Actions 配置

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -e ".[dev]"
          pytest --cov=app
```

---

## 测试数据

### 示例测试数据

```python
# 可用于手动测试的数据

# 收入
transaction = {
    "amount": 10000,
    "date": "2024-01-15",
    "category": "salary",
    "note": "Monthly salary"
}
# 期望：自动分类为 income

# 支出
transaction = {
    "amount": 50,
    "date": "2024-01-16",
    "category": "food",
    "note": "Lunch at restaurant"
}
# 期望：自动分类为 expense
```
