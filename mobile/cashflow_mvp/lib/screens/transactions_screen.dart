import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../models/transaction.dart';
import '../providers/data_provider.dart';

class TransactionsScreen extends StatefulWidget {
  const TransactionsScreen({super.key});

  @override
  State<TransactionsScreen> createState() => _TransactionsScreenState();
}

class _TransactionsScreenState extends State<TransactionsScreen> {
  @override
  void initState() {
    super.initState();
    // Load data when screen initializes
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadTransactions();
    });
  }

  Future<void> _deleteTransaction(int id) async {
    final success = await context.read<DataProvider>().deleteTransaction(id);
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('交易已删除')),
        );
      } else {
        final error = context.read<DataProvider>().transactionsError;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(error ?? '删除失败'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _refreshTransactions() async {
    await context.read<DataProvider>().loadTransactions();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('交易记录'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshTransactions,
          ),
        ],
      ),
      body: Consumer<DataProvider>(
        builder: (context, provider, child) {
          return _buildBody(provider);
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddTransactionDialog,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody(DataProvider provider) {
    // Show loading indicator
    if (provider.isLoadingTransactions && provider.transactions.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('加载中...', style: TextStyle(color: Colors.grey)),
          ],
        ),
      );
    }

    // Show error state with retry button
    if (provider.transactionsError != null && provider.transactions.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.error_outline,
                size: 64,
                color: Colors.red,
              ),
              const SizedBox(height: 16),
              Text(
                provider.transactionsError!,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.red,
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _refreshTransactions,
                icon: const Icon(Icons.refresh),
                label: const Text('重试'),
              ),
            ],
          ),
        ),
      );
    }

    // Show empty state
    if (provider.transactions.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.receipt_long_outlined,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: 16),
            const Text(
              '暂无交易记录',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            const Text(
              '点击右下角添加',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
          ],
        ),
      );
    }

    // Show data with pull-to-refresh
    return RefreshIndicator(
      onRefresh: _refreshTransactions,
      child: ListView.builder(
        itemCount: provider.transactions.length,
        itemBuilder: (context, index) {
          final transaction = provider.transactions[index];
          return _buildTransactionItem(transaction);
        },
      ),
    );
  }

  Widget _buildTransactionItem(Transaction transaction) {
    final isIncome = transaction.cashflowType == 'income';
    final color = isIncome ? Colors.green : Colors.red;
    final sign = isIncome ? '+' : '-';

    return Dismissible(
      key: Key(transaction.id.toString()),
      direction: DismissDirection.endToStart,
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 16),
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      onDismissed: (_) => _deleteTransaction(transaction.id!),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withAlpha((0.1 * 255).toInt()),
          child: Text(
            transaction.cashflowTypeIcon,
            style: TextStyle(color: color),
          ),
        ),
        title: Text(transaction.category),
        subtitle: Text(
          '${transaction.date}${transaction.note != null && transaction.note!.isNotEmpty ? ' · ${transaction.note}' : ''}',
          style: const TextStyle(fontSize: 12),
        ),
        trailing: Text(
          '$sign¥${transaction.amount.toStringAsFixed(2)}',
          style: TextStyle(
            color: color,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  void _showAddTransactionDialog() {
    showDialog(
      context: context,
      builder: (context) => const AddTransactionDialog(),
    );
  }
}

class AddTransactionDialog extends StatefulWidget {
  const AddTransactionDialog({super.key});

  @override
  State<AddTransactionDialog> createState() => _AddTransactionDialogState();
}

class _AddTransactionDialogState extends State<AddTransactionDialog> {
  final _formKey = GlobalKey<FormState>();
  final _amountController = TextEditingController();
  final _noteController = TextEditingController();

  String _cashflowType = 'expense';
  String? _selectedCategory;
  DateTime _selectedDate = DateTime.now();
  bool _isSubmitting = false;

  final List<Map<String, String>> _cashflowTypes = [
    {'value': 'income', 'label': '收入'},
    {'value': 'expense', 'label': '支出'},
    {'value': 'investment', 'label': '投资'},
    {'value': 'liability_repayment', 'label': '负债还款'},
  ];

  final Map<String, List<String>> _categoriesByType = {
    'income': ['工资', '奖金', '投资收益', '兼职', '红包', '其他收入'],
    'expense': ['餐饮', '交通', '购物', '娱乐', '医疗', '教育', '房租', '水电', '其他支出'],
    'investment': ['股票', '基金', '定期存款', '保险', '其他投资'],
    'liability_repayment': ['信用卡', '房贷', '车贷', '其他贷款'],
  };

  @override
  void dispose() {
    _amountController.dispose();
    _noteController.dispose();
    super.dispose();
  }

  Future<void> _selectDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      setState(() => _selectedDate = picked);
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSubmitting = true);

    final transaction = Transaction(
      amount: double.parse(_amountController.text),
      date: DateFormat('yyyy-MM-dd').format(_selectedDate),
      note: _noteController.text.isEmpty ? null : _noteController.text,
      category: _selectedCategory ?? '未分类',
      cashflowType: _cashflowType,
    );

    final success = await context.read<DataProvider>().createTransaction(transaction);

    if (mounted) {
      setState(() => _isSubmitting = false);

      if (success) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('交易已添加')),
        );
      } else {
        final error = context.read<DataProvider>().transactionsError;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(error ?? '添加失败'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('添加交易'),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Type selector - required
              DropdownButtonFormField<String>(
                value: _cashflowType,
                decoration: const InputDecoration(labelText: '类型 *'),
                items: _cashflowTypes.map((type) {
                  return DropdownMenuItem(
                    value: type['value']!,
                    child: Text(type['label']!),
                  );
                }).toList(),
                onChanged: (value) {
                  if (value != null) {
                    setState(() {
                      _cashflowType = value;
                      _selectedCategory = null;
                    });
                  }
                },
              ),
              const SizedBox(height: 8),
              // Amount - required
              TextFormField(
                controller: _amountController,
                decoration: const InputDecoration(
                  labelText: '金额 *',
                  prefixText: '¥',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入金额';
                  }
                  if (double.tryParse(value) == null) {
                    return '请输入有效数字';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 8),
              // Category dropdown - optional
              DropdownButtonFormField<String?>(
                value: _selectedCategory,
                decoration: const InputDecoration(
                  labelText: '分类（可选）',
                ),
                items: [
                  const DropdownMenuItem<String?>(value: null, child: Text('未分类')),
                  ..._categoriesByType[_cashflowType]!.map((cat) {
                    return DropdownMenuItem<String?>(value: cat, child: Text(cat));
                  }),
                ],
                onChanged: (value) => setState(() => _selectedCategory = value),
              ),
              const SizedBox(height: 8),
              // Date picker
              ListTile(
                title: const Text('日期'),
                subtitle: Text(DateFormat('yyyy-MM-dd').format(_selectedDate)),
                trailing: const Icon(Icons.calendar_today),
                onTap: _selectDate,
              ),
              // Note - optional
              TextFormField(
                controller: _noteController,
                decoration: const InputDecoration(
                  labelText: '备注（可选）',
                ),
                maxLines: 2,
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: _isSubmitting ? null : () => Navigator.of(context).pop(),
          child: const Text('取消'),
        ),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _submit,
          child: _isSubmitting
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Text('保存'),
        ),
      ],
    );
  }
}
