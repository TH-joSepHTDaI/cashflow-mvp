import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/liability.dart';
import '../providers/data_provider.dart';

class LiabilitiesScreen extends StatefulWidget {
  const LiabilitiesScreen({super.key});

  @override
  State<LiabilitiesScreen> createState() => _LiabilitiesScreenState();
}

class _LiabilitiesScreenState extends State<LiabilitiesScreen> {
  @override
  void initState() {
    super.initState();
    // Load data when screen initializes
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadLiabilities();
    });
  }

  Future<void> _deleteLiability(int id) async {
    final success = await context.read<DataProvider>().deleteLiability(id);
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('负债已删除')),
        );
      } else {
        final error = context.read<DataProvider>().liabilitiesError;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(error ?? '删除失败'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _refreshLiabilities() async {
    await context.read<DataProvider>().loadLiabilities();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('负债管理'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshLiabilities,
          ),
        ],
      ),
      body: Consumer<DataProvider>(
        builder: (context, provider, child) {
          return _buildBody(provider);
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddLiabilityDialog(),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody(DataProvider provider) {
    // Show loading indicator
    if (provider.isLoadingLiabilities && provider.liabilities.isEmpty) {
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
    if (provider.liabilitiesError != null && provider.liabilities.isEmpty) {
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
                provider.liabilitiesError!,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.red,
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _refreshLiabilities,
                icon: const Icon(Icons.refresh),
                label: const Text('重试'),
              ),
            ],
          ),
        ),
      );
    }

    // Show data with pull-to-refresh
    return RefreshIndicator(
      onRefresh: _refreshLiabilities,
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: _buildTotalCard(provider),
          ),
          if (provider.liabilities.isEmpty)
            const SliverFillRemaining(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.credit_card_outlined,
                      size: 64,
                      color: Colors.grey,
                    ),
                    SizedBox(height: 16),
                    Text(
                      '暂无负债',
                      style: TextStyle(fontSize: 16, color: Colors.grey),
                    ),
                    SizedBox(height: 8),
                    Text(
                      '点击右下角添加',
                      style: TextStyle(fontSize: 14, color: Colors.grey),
                    ),
                  ],
                ),
              ),
            )
          else
            SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  final liability = provider.liabilities[index];
                  return _buildLiabilityItem(liability);
                },
                childCount: provider.liabilities.length,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildTotalCard(DataProvider provider) {
    return Card(
      margin: const EdgeInsets.all(16),
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text(
              '总负债',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Text(
              '¥${provider.totalLiabilitiesValue.toStringAsFixed(2)}',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.red,
              ),
            ),
            const SizedBox(height: 8),
            Text('${provider.liabilities.length} 项负债'),
          ],
        ),
      ),
    );
  }

  Widget _buildLiabilityItem(Liability liability) {
    return Dismissible(
      key: Key(liability.id.toString()),
      direction: DismissDirection.endToStart,
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 16),
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      onDismissed: (_) => _deleteLiability(liability.id!),
      child: ListTile(
        leading: CircleAvatar(
          child: Text(liability.liabilityTypeIcon),
        ),
        title: Text(liability.name),
        subtitle: Text(liability.liabilityTypeDisplay),
        trailing: Text(
          '¥${liability.value.toStringAsFixed(2)}',
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  void _showAddLiabilityDialog() {
    showDialog(
      context: context,
      builder: (context) => const AddLiabilityDialog(),
    );
  }
}

class AddLiabilityDialog extends StatefulWidget {
  const AddLiabilityDialog({super.key});

  @override
  State<AddLiabilityDialog> createState() => _AddLiabilityDialogState();
}

class _AddLiabilityDialogState extends State<AddLiabilityDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _valueController = TextEditingController();

  String _liabilityType = 'credit_card';
  bool _isSubmitting = false;

  final List<Map<String, String>> _liabilityTypes = [
    {'value': 'credit_card', 'label': '信用卡'},
    {'value': 'mortgage', 'label': '房贷'},
    {'value': 'car_loan', 'label': '车贷'},
    {'value': 'consumer_loan', 'label': '消费贷'},
    {'value': 'other', 'label': '其他'},
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _valueController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSubmitting = true);

    final liability = Liability(
      name: _nameController.text,
      liabilityType: _liabilityType,
      value: double.parse(_valueController.text),
    );

    final success = await context.read<DataProvider>().createLiability(liability);

    if (mounted) {
      setState(() => _isSubmitting = false);

      if (success) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('负债已添加')),
        );
      } else {
        final error = context.read<DataProvider>().liabilitiesError;
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
      title: const Text('添加负债'),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(labelText: '负债名称'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入负债名称';
                  }
                  return null;
                },
              ),
              DropdownButtonFormField<String>(
                value: _liabilityType,
                decoration: const InputDecoration(labelText: '负债类型'),
                items: _liabilityTypes.map((type) {
                  return DropdownMenuItem(
                    value: type['value'],
                    child: Text(type['label']!),
                  );
                }).toList(),
                onChanged: (value) => setState(() => _liabilityType = value!),
              ),
              TextFormField(
                controller: _valueController,
                decoration: const InputDecoration(
                  labelText: '当前余额',
                  prefixText: '¥',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入余额';
                  }
                  if (double.tryParse(value) == null) {
                    return '请输入有效数字';
                  }
                  return null;
                },
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
