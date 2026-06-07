import 'package:flutter/material.dart';
import '../services/api_service.dart';

class BalanceSheetScreen extends StatefulWidget {
  const BalanceSheetScreen({super.key});

  @override
  State<BalanceSheetScreen> createState() => _BalanceSheetScreenState();
}

class _BalanceSheetScreenState extends State<BalanceSheetScreen> {
  Map<String, dynamic> _balanceSheet = {};
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadBalanceSheet();
  }

  Future<void> _loadBalanceSheet() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final balanceSheet = await ApiService.getBalanceSheet();
      setState(() {
        _balanceSheet = balanceSheet;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('资产负债表'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadBalanceSheet,
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('错误: $_error'),
            ElevatedButton(
              onPressed: _loadBalanceSheet,
              child: const Text('重试'),
            ),
          ],
        ),
      );
    }

    // Handle both summary endpoint (flat structure) and full endpoint (nested structure)
    final summary = _balanceSheet['summary'] ?? _balanceSheet;
    final totalAssets = (summary['total_assets'] ?? _balanceSheet['total_assets'] ?? 0.0).toDouble();
    final totalLiabilities = (summary['total_liabilities'] ?? _balanceSheet['total_liabilities'] ?? 0.0).toDouble();
    final netWorth = (summary['net_worth'] ?? _balanceSheet['net_worth'] ?? 0.0).toDouble();
    final assetCount = _balanceSheet['asset_count'] ?? _balanceSheet['assets']?['count'] ?? 0;
    final liabilityCount = _balanceSheet['liability_count'] ?? _balanceSheet['liabilities']?['count'] ?? 0;

    return RefreshIndicator(
      onRefresh: _loadBalanceSheet,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildNetWorthCard(netWorth),
          const SizedBox(height: 16),
          _buildAssetsCard(totalAssets, assetCount),
          const SizedBox(height: 16),
          _buildLiabilitiesCard(totalLiabilities, liabilityCount),
          const SizedBox(height: 16),
          _buildBreakdownSection(),
        ],
      ),
    );
  }

  Widget _buildNetWorthCard(double netWorth) {
    return Card(
      elevation: 4,
      color: netWorth >= 0 ? Colors.green.shade50 : Colors.red.shade50,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const Text(
              '净资产',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            Text(
              '¥${netWorth.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 40,
                fontWeight: FontWeight.bold,
                color: netWorth >= 0 ? Colors.green : Colors.red,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAssetsCard(double totalAssets, int count) {
    return Card(
      elevation: 2,
      child: ListTile(
        leading: const CircleAvatar(
          backgroundColor: Colors.green,
          child: Icon(Icons.trending_up, color: Colors.white),
        ),
        title: const Text('总资产'),
        subtitle: Text('$count 项资产'),
        trailing: Text(
          '¥${totalAssets.toStringAsFixed(2)}',
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.green,
          ),
        ),
      ),
    );
  }

  Widget _buildLiabilitiesCard(double totalLiabilities, int count) {
    return Card(
      elevation: 2,
      child: ListTile(
        leading: const CircleAvatar(
          backgroundColor: Colors.red,
          child: Icon(Icons.trending_down, color: Colors.white),
        ),
        title: const Text('总负债'),
        subtitle: Text('$count 项负债'),
        trailing: Text(
          '¥${totalLiabilities.toStringAsFixed(2)}',
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Colors.red,
          ),
        ),
      ),
    );
  }

  Widget _buildBreakdownSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '资产分布',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        _buildTypeBreakdown('asset'),
        const SizedBox(height: 16),
        const Text(
          '负债分布',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        _buildTypeBreakdown('liability'),
      ],
    );
  }

  Widget _buildTypeBreakdown(String type) {
    // This would show breakdown by type if we had the detailed endpoint
    // For now, show a placeholder
    return const Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Center(
          child: Text(
            '详细分类数据可在资产/负债页面查看',
            style: TextStyle(color: Colors.grey),
          ),
        ),
      ),
    );
  }
}
