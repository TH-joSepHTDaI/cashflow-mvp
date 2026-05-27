# Cashflow MVP Mobile

Flutter frontend for the cashflow app.

## Setup

```bash
flutter pub get
```

## Run

```bash
flutter run
```

## Configure API

Edit `lib/services/api_service.dart`:

```dart
// iOS Simulator
static const String baseUrl = 'http://localhost:8000';

// Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000';
```

## Project Structure

```
lib/
├── main.dart
├── models/
│   ├── transaction.dart
│   ├── asset.dart
│   └── liability.dart
├── services/
│   └── api_service.dart
└── screens/
    ├── home_screen.dart
    ├── transactions_screen.dart
    ├── assets_screen.dart
    ├── liabilities_screen.dart
    ├── balance_sheet_screen.dart
    └── cashflow_screen.dart
```
