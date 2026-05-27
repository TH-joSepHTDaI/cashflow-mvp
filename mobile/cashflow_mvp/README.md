# Cashflow MVP - Flutter App

个人记账应用的 Flutter 前端。

## 功能

- 📊 **仪表盘** - 净资产和本月现金流概览
- 💰 **交易记录** - 收入、支出、投资、负债还款
- 🏦 **资产管理** - 现金、银行存款、基金股票、房产
- 💳 **负债管理** - 信用卡、房贷、车贷、消费贷
- 📈 **资产负债表** - 净资产计算
- 📉 **现金流分析** - 按月查看收支情况

## 安装

### 1. 安装 Flutter

```bash
# macOS (使用 Homebrew)
brew install flutter

# 或者从官网下载: https://flutter.dev/docs/get-started/install
```

### 2. 安装依赖

```bash
cd mobile/cashflow_mvp
flutter pub get
```

### 3. 配置后端地址

编辑 `lib/services/api_service.dart`:

```dart
// Android 模拟器
static const String baseUrl = 'http://10.0.2.2:8000';

// iOS 模拟器
static const String baseUrl = 'http://localhost:8000';

// 真机 (使用电脑 IP)
static const String baseUrl = 'http://192.168.1.xxx:8000';
```

### 4. 启动后端服务

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 运行 Flutter 应用

```bash
# iOS 模拟器
flutter run

# Android 模拟器
flutter run

# 选择设备
flutter devices
flutter run -d <device_id>
```

## 构建发布版本

```bash
# iOS
flutter build ios --release

# Android
flutter build apk --release
flutter build appbundle --release
```

## 项目结构

```
lib/
├── main.dart                 # 应用入口
├── models/                   # 数据模型
│   ├── transaction.dart
│   ├── asset.dart
│   └── liability.dart
├── services/                 # API 服务
│   └── api_service.dart
├── screens/                  # 页面
│   ├── home_screen.dart
│   ├── transactions_screen.dart
│   ├── assets_screen.dart
│   ├── liabilities_screen.dart
│   ├── balance_sheet_screen.dart
│   └── cashflow_screen.dart
└── widgets/                  # 可复用组件 (待添加)
```

## 截图

(待添加)

## 开发计划

- [x] 基础项目结构
- [x] 交易记录功能
- [x] 资产管理功能
- [x] 负债管理功能
- [x] 资产负债表
- [x] 现金流分析
- [ ] 图表展示
- [ ] 数据同步
- [ ] 本地缓存
- [ ] 用户认证
