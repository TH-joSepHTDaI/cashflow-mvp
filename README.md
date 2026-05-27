# 💰 Cashflow MVP

> 一个极简的个人记账应用，帮助你追踪收入、支出、资产和负债。

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.0+-blue.svg)](https://flutter.dev)

---

## 📸 项目截图

> 截图将在首次运行后添加

---

## ✨ 功能特性

### 📊 财务管理
- **交易记录** - 记录每一笔收入、支出、投资和负债还款
- **智能分类** - 根据关键词自动识别交易类型（支持中英文）
- **资产管理** - 追踪现金、银行存款、股票基金、房产等资产
- **负债管理** - 管理信用卡、房贷、车贷等负债

### 📈 数据洞察
- **资产负债表** - 实时计算净资产（资产 - 负债）
- **现金流分析** - 按月查看收支情况，了解财务健康状况
- **分类统计** - 按类别查看消费分布

### 📱 跨平台支持
- **后端** - FastAPI + SQLite，轻量高效
- **移动端** - Flutter 构建，支持 iOS 和 Android

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面层 (Flutter)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  仪表盘   │ │ 交易记录  │ │ 资产负债  │ │ 现金流   │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/REST API
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    API 服务层 (FastAPI)                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │ /transactions│ │  /assets    │ │  /liabilities   │   │
│  │  交易API    │ │  资产API    │ │   负债API       │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
│  ┌─────────────┐ ┌─────────────┐                        │
│  │/balance-sheet│ │  /cashflow  │                        │
│  │  资产负债   │ │  现金流API  │                        │
│  └─────────────┘ └─────────────┘                        │
└─────────────────────────┬───────────────────────────────┘
                          │ SQLModel
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    数据存储层 (SQLite)                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │transactions │ │    assets   │ │   liabilities   │   │
│  │  交易表     │ │   资产表    │ │    负债表       │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式一：只运行后端（推荐初学者）

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -e ".[dev]"

# 4. 启动服务
uvicorn app.main:app --reload

# 5. 打开文档
open http://localhost:8000/docs
```

### 方式二：完整体验（后端 + 移动端）

#### 第一步：启动后端

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 第二步：启动移动端

```bash
# 新终端窗口
cd mobile/cashflow_mvp

# 安装依赖
flutter pub get

# 运行（选择你的设备）
flutter run
```

---

## 📁 项目结构

```
cashflow-mvp/
├── 📄 README.md                 # 本文件
├── 📄 .env.example              # 环境变量示例
├── 📁 backend/                  # 后端服务
│   ├── 📄 README.md            # 后端详细文档
│   ├── 📁 app/                 # 应用代码
│   │   ├── 📄 main.py          # 应用入口
│   │   ├── 📄 models.py        # 数据模型
│   │   ├── 📄 database.py      # 数据库配置
│   │   ├── 📄 classifier.py    # 智能分类器
│   │   ├── 📁 routers/         # API 路由
│   │   │   ├── 📄 transactions.py
│   │   │   ├── 📄 assets.py
│   │   │   ├── 📄 liabilities.py
│   │   │   ├── 📄 balance_sheet.py
│   │   │   └── 📄 cashflow.py
│   │   └── 📁 ...
│   └── 📁 tests/               # 测试代码
│
├── 📁 mobile/                   # 移动端应用
│   └── 📁 cashflow_mvp/
│       ├── 📄 README.md        # 移动端文档
│       ├── 📁 lib/
│       │   ├── 📄 main.dart    # 应用入口
│       │   ├── 📁 models/      # 数据模型
│       │   ├── 📁 services/    # API 服务
│       │   ├── 📁 screens/     # 页面
│       │   └── 📁 ...
│       └── 📁 ...
│
├── 📁 docs/                     # 项目文档
│   ├── 📄 product_requirements.md
│   ├── 📄 api_spec.md
│   ├── 📄 data_model.md
│   └── 📄 ...
│
└── 📁 scripts/                  # 实用脚本
    ├── 📄 run_backend_tests.sh
    └── 📄 run_mobile_tests.sh
```

---

## 🧪 运行测试

### 后端测试

```bash
cd backend
source .venv/bin/activate
pytest -v

# 查看覆盖率
pytest --cov=app --cov-report=html
```

### 移动端测试

```bash
cd mobile/cashflow_mvp
flutter test
```

---

## 📚 文档导航

| 文档 | 内容 |
|------|------|
| [后端文档](backend/README.md) | API 详细说明、部署指南 |
| [移动端文档](mobile/cashflow_mvp/README.md) | Flutter 开发指南 |
| [产品需求](docs/product_requirements.md) | 功能需求列表 |
| [API 规范](docs/api_spec.md) | REST API 详细规范 |
| [数据模型](docs/data_model.md) | 数据库设计说明 |

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 💡 常见问题

**Q: 数据存储在哪里？**  
A: 默认使用 SQLite，数据库文件在 `backend/data/cashflow.db`

**Q: 如何备份数据？**  
A: 直接复制 `backend/data/cashflow.db` 文件即可

**Q: 支持多用户吗？**  
A: 当前 MVP 版本为单用户设计，多用户功能在规划中

---

> Made with ❤️ by TH-joSepHTDaI
