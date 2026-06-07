import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';

class CashflowScreen extends StatefulWidget {
  const CashflowScreen({super.key});

  @override
  State<CashflowScreen> createState() => _CashflowScreenState();
}

class _CashflowScreenState extends State<CashflowScreen> {
  Map<String, dynamic> _cashflow = {};
  bool _isLoading = true;
  String? _error;
  DateTime _selectedMonth = DateTime.now();

  @override
  void initState() {
    super.initState();
    _loadCashflow();
  }

  Future<void> _loadCashflow() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final month = DateFormat('yyyy-MM').format(_selectedMonth);
      final cashflow = await ApiService.getMonthlyCashflow(month);
      setState(() {
        _cashflow = cashflow;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _selectMonth() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedMonth,
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
      initialDatePickerMode: DatePickerMode.year,
    );
    if (picked != null) {
      setState(() => _selectedMonth = picked);
      _loadCashflow();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('现金流分析'),
        actions: [
          IconButton(
            icon: const Icon(Icons.calendar_today),
            onPressed: _selectMonth,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadCashflow,
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
              onPressed: _loadCashflow,
              child: const Text('重试'),
            ),
          ],
        ),
      );
    }

    final income = (_cashflow['total_income'] ?? 0.0).toDouble();
    final expense = (_cashflow['total_expense'] ?? 0.0).toDouble();
    final investment = (_cashflow['total_investment'] ?? 0.0).toDouble();
    final liabilityRepayment = (_cashflow['total_liability_repayment'] ?? 0.0).toDouble();
    final netCashflow = (_cashflow['net_cashflow'] ?? 0.0).toDouble();
    final transactionCount = _cashflow['transaction_count'] ?? 0;

    return RefreshIndicator(
      onRefresh: _loadCashflow,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildMonthSelector(),
          const SizedBox(height: 16),
          _buildNetCashflowCard(netCashflow),
          const SizedBox(height: 16),
          _buildIncomeCard(income),
          const SizedBox(height: 8),
          _buildExpenseCard(expense),
          const SizedBox(height: 8),
          _buildInvestmentCard(investment),
          const SizedBox(height: 8),
          _buildLiabilityCard(liabilityRepayment),
          const SizedBox(height: 16),
          _buildTransactionCount(transactionCount),
        ],
      ),
    );
  }

  Widget _buildMonthSelector() {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.calendar_month),
        title: Text(
          DateFormat('yyyy年MM月').format(_selectedMonth),
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        trailing: const Icon(Icons.arrow_drop_down),
        onTap: _selectMonth,
      ),
    );
  }

  Widget _buildNetCashflowCard(double netCashflow) {
    final isPositive = netCashflow >= 0;
    return Card(
      elevation: 4,
      color: isPositive ? Colors.green.shade50 : Colors.red.shade50,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const Text(
              '净现金流',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            Text(
              '${isPositive ? '+' : ''}¥${netCashflow.toStringAsFixed(2)}',
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
                color: isPositive ? Colors.green : Colors.red,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIncomeCard(double income) {
    return _buildCashflowItemCard(
      '收入',
      income,
      Colors.green,
      Icons.arrow_downward,
    );
  }

  Widget _buildExpenseCard(double expense) {
    return _buildCashflowItemCard(
      '支出',
      expense,
      Colors.red,
      Icons.arrow_upward,
    );
  }

  Widget _buildInvestmentCard(double investment) {
    return _buildCashflowItemCard(
      '投资',
      investment,
      Colors.blue,
      Icons.trending_up,
    );
  }

  Widget _buildLiabilityCard(double liability) {
    return _buildCashflowItemCard(
      '负债还款',
      liability,
      Colors.orange,
      Icons.credit_card,
    );
  }

  Widget _buildCashflowItemCard(
    String label,
    double amount,
    Color color,
    IconData icon,
  ) {
    return Card(
      elevation: 2,
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.1),
          child: Icon(icon, color: color),
        ),
        title: Text(label),
        trailing: Text(
          '¥${amount.toStringAsFixed(2)}',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ),
    );
  }

  Widget _buildTransactionCount(int count) {
    return Center(
      child: Text(
        '本月共 $count 笔交易',
        style: const TextStyle(color: Colors.grey),
      ),
    );
  }
}
