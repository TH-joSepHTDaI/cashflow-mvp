// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. Additionally, you can find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:cashflow_mvp/main.dart';
import 'package:cashflow_mvp/providers/data_provider.dart';

void main() {
  testWidgets('CashflowApp renders correctly', (WidgetTester tester) async {
    // Build our app with the required provider and trigger a frame.
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (context) => DataProvider(),
        child: const CashflowApp(),
      ),
    );

    // Verify that the app title is displayed in the AppBar.
    expect(find.text('Cashflow MVP'), findsOneWidget);

    // Verify that the loading indicator is shown initially.
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('Bottom navigation has correct items', (WidgetTester tester) async {
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (context) => DataProvider(),
        child: const CashflowApp(),
      ),
    );

    // Wait for the widget to settle.
    await tester.pump();

    // Verify bottom navigation items exist.
    expect(find.text('概览'), findsOneWidget);
    expect(find.text('交易'), findsOneWidget);
    expect(find.text('资产'), findsOneWidget);
    expect(find.text('负债'), findsOneWidget);
    expect(find.text('现金流'), findsOneWidget);
  });
}
