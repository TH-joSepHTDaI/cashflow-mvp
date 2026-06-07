import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'transactions_screen.dart';
import 'assets_screen.dart';
import 'liabilities_screen.dart';
import 'balance_sheet_screen.dart';
import 'cashflow_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isLoading = true;
  bool _isConnected = false;
  Map<String, dynamic> _balanceSheet = {};
  Map<String, dynamic> _monthlyCashflow = {};

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    
    try {
      final isConnected = await ApiService.checkHealth();
      if (isConnected) {
        final balanceSheet = await ApiService.getBalanceSheet();
        final now = DateTime.now();
        final month = '${now.year}-${now.month.toString().padLeft(2, '0')}';
        final cashflow = await ApiService.getMonthlyCashflow(month);
        
        setState(() {
          _isConnected = true;
          _balanceSheet = balanceSheet;
          _monthlyCashflow = cashflow;
        });
      } else {
        setState(() => _isConnected = false);
      }
    } catch (e) {
      setState(() => _isConnected = false);
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cashflow MVP'),
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadData,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : !_isConnected
              ? _buildConnectionError()
              : _buildDashboard(),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: 0,
        onTap: (index) {
          switch (index) {
            case 1:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const TransactionsScreen()),
              );
              break;
            case 2:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AssetsScreen()),
              );
              break;
            case 3:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const LiabilitiesScreen()),
              );
              break;
            case 4:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const CashflowScreen()),
              );
              break;
          }
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: '概览',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt_long),
            label: '交易',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_balance),
            label: '资产',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.credit_card),
            label: '负债',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.trending_up),
            label: '现金流',
          ),
        ],
      ),
    );
  }

  Widget _buildConnectionError() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline, size: 64, color: Colors.red),
          const SizedBox(height: 16),
          const Text(
            '无法连接到服务器',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text('请确保后端服务正在运行'),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _loadData,
            child: const Text('重试'),
          ),
        ],
      ),
    );
  }

  Widget _buildDashboard() {
    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildNetWorthCard(),
          const SizedBox(height: 16),
          _buildMonthlyCashflowCard(),
          const SizedBox(height: 16),
          _buildQuickActions(),
        ],
      ),
    );
  }

  Widget _buildNetWorthCard() {
    final netWorth = (_balanceSheet['net_worth'] ?? 0.0).toDouble();
    final totalAssets = (_balanceSheet['total_assets'] ?? 0.0).toDouble();
    final totalLiabilities = (_balanceSheet['total_liabilities'] ?? 0.0).toDouble();

    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '净资产',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Text(
              '¥${netWorth.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: netWorth >= 0 ? Colors.green : Colors.red,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildMiniStat('总资产', totalAssets, Colors.green),
                ),
                Expanded(
                  child: _buildMiniStat('总负债', totalLiabilities, Colors.red),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMiniStat(String label, double value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        Text(
          '¥${value.toStringAsFixed(0)}',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }

  Widget _buildMonthlyCashflowCard() {
    final income = (_monthlyCashflow['total_income'] ?? 0.0).toDouble();
    final expense = (_monthlyCashflow['total_expense'] ?? 0.0).toDouble();
    final netCashflow = (_monthlyCashflow['net_cashflow'] ?? 0.0).toDouble();

    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  '本月现金流',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const BalanceSheetScreen(),
                      ),
                    );
                  },
                  child: const Text('查看详情'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildCashflowItem('收入', income, Colors.green),
                ),
                Expanded(
                  child: _buildCashflowItem('支出', expense, Colors.red),
                ),
                Expanded(
                  child: _buildCashflowItem(
                    '净现金流',
                    netCashflow,
                    netCashflow >= 0 ? Colors.green : Colors.red,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCashflowItem(String label, double value, Color color) {
    return Column(
      children: [
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        const SizedBox(height: 4),
        Text(
          '¥${value.toStringAsFixed(0)}',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }

  Widget _buildQuickActions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '快速操作',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: _buildActionButton(
                '记一笔',
                Icons.add_circle,
                Colors.blue,
                () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const TransactionsScreen(),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: _buildActionButton(
                '资产负债表',
                Icons.account_balance_wallet,
                Colors.purple,
                () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const BalanceSheetScreen(),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActionButton(
    String label,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 24),
          child: Column(
            children: [
              Icon(icon, size: 32, color: color),
              const SizedBox(height: 8),
              Text(label),
            ],
          ),
        ),
      ),
    );
  }
}
