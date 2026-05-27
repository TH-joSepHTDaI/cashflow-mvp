# 💻 Cashflow MVP Backend

FastAPI 后端服务，提供 RESTful API 支持。

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 1. 进入目录
cd backend

# 2. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -e ".[dev]"

# 4. 启动服务
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 启动

---

## 📚 API 文档

启动服务后访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 API 端点一览

### 交易管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/transactions/` | 列出所有交易 |
| POST | `/api/transactions/` | 创建交易（自动分类） |
| GET | `/api/transactions/{id}` | 获取单个交易 |
| PUT | `/api/transactions/{id}` | 更新交易 |
| DELETE | `/api/transactions/{id}` | 删除交易 |

**查询参数：**
- `?month=2024-01` - 按月筛选

### 资产管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/assets/` | 列出所有资产 |
| POST | `/api/assets/` | 创建资产 |
| GET | `/api/assets/{id}` | 获取单个资产 |
| PUT | `/api/assets/{id}` | 更新资产 |
| DELETE | `/api/assets/{id}` | 删除资产 |

### 负债管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/liabilities/` | 列出所有负债 |
| POST | `/api/liabilities/` | 创建负债 |
| GET | `/api/liabilities/{id}` | 获取单个负债 |
| PUT | `/api/liabilities/{id}` | 更新负债 |
| DELETE | `/api/liabilities/{id}` | 删除负债 |

### 财务报表

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/balance-sheet/` | 完整资产负债表 |
| GET | `/api/balance-sheet/summary` | 简要汇总 |
| GET | `/api/balance-sheet/assets/by-type/{type}` | 按类型查资产 |
| GET | `/api/balance-sheet/liabilities/by-type/{type}` | 按类型查负债 |

### 现金流分析

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/cashflow/monthly/{year_month}` | 单月现金流 |
| GET | `/api/cashflow/monthly/range` | 多月现金流范围 |
| GET | `/api/cashflow/summary` | 现金流汇总 |
| GET | `/api/cashflow/by-category/{year_month}` | 按分类统计 |

---

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 详细输出
pytest -v

# 运行特定测试文件
pytest tests/test_transactions.py -v

# 查看覆盖率
pytest --cov=app --cov-report=html
# 然后打开 htmlcov/index.html
```

---

## 📖 代码结构

```
app/
├── __init__.py          # 包初始化
├── main.py              # FastAPI 应用入口
├── database.py          # 数据库连接和配置
├── models.py            # SQLModel 数据模型
├── schemas.py           # Pydantic 数据验证模式
├── classifier.py        # 交易自动分类器
└── routers/             # API 路由模块
    ├── __init__.py
    ├── transactions.py  # 交易 API
    ├── assets.py        # 资产 API
    ├── liabilities.py   # 负债 API
    ├── balance_sheet.py # 资产负债表 API
    └── cashflow.py      # 现金流 API
```

---

## 🔧 配置说明

### 数据库

默认使用 SQLite，数据库文件位置：`data/cashflow.db`

如需更改，修改 `app/database.py` 中的 `DATABASE_PATH`

### CORS

默认允许所有来源，生产环境请修改 `app/main.py`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 故障排查

### 问题：端口被占用

```bash
# 查找占用 8000 端口的进程
lsof -i :8000

# 使用其他端口
uvicorn app.main:app --reload --port 8080
```

### 问题：数据库锁定

SQLite 不支持并发写入，确保只有一个服务实例运行。

### 问题：模块导入错误

```bash
# 确保在 backend 目录下
pwd  # 应该显示 .../cashflow-mvp/backend

# 重新安装
pip install -e ".[dev]"
```

---

## 📦 部署

### 使用 Docker（推荐）

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e ".[dev]"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t cashflow-backend .
docker run -p 8000:8000 cashflow-backend
```

### 使用 Gunicorn（生产环境）

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📝 开发计划

- [x] 基础 CRUD API
- [x] 自动分类
- [x] 资产负债表
- [x] 现金流分析
- [ ] 用户认证 (JWT)
- [ ] 数据导出 (CSV/Excel)
- [ ] 数据库迁移 (Alembic)
- [ ] 性能优化
