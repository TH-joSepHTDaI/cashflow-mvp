import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/asset.dart';
import '../providers/data_provider.dart';

class AssetsScreen extends StatefulWidget {
  const AssetsScreen({super.key});

  @override
  State<AssetsScreen> createState() => _AssetsScreenState();
}

class _AssetsScreenState extends State<AssetsScreen> {
  @override
  void initState() {
    super.initState();
    // Load data when screen initializes
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadAssets();
    });
  }

  Future<void> _deleteAsset(int id) async {
    final success = await context.read<DataProvider>().deleteAsset(id);
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('资产已删除')),
        );
      } else {
        final error = context.read<DataProvider>().assetsError;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(error ?? '删除失败'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _refreshAssets() async {
    await context.read<DataProvider>().loadAssets();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('资产管理'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshAssets,
          ),
        ],
      ),
      body: Consumer<DataProvider>(
        builder: (context, provider, child) {
          return _buildBody(provider);
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddAssetDialog(),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody(DataProvider provider) {
    // Show loading indicator
    if (provider.isLoadingAssets && provider.assets.isEmpty) {
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
    if (provider.assetsError != null && provider.assets.isEmpty) {
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
                provider.assetsError!,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.red,
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _refreshAssets,
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
      onRefresh: _refreshAssets,
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: _buildTotalCard(provider),
          ),
          if (provider.assets.isEmpty)
            const SliverFillRemaining(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.account_balance_wallet_outlined,
                      size: 64,
                      color: Colors.grey,
                    ),
                    SizedBox(height: 16),
                    Text(
                      '暂无资产',
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
                  final asset = provider.assets[index];
                  return _buildAssetItem(asset);
                },
                childCount: provider.assets.length,
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
              '总资产',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Text(
              '¥${provider.totalAssetsValue.toStringAsFixed(2)}',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            const SizedBox(height: 8),
            Text('${provider.assets.length} 项资产'),
          ],
        ),
      ),
    );
  }

  Widget _buildAssetItem(Asset asset) {
    return Dismissible(
      key: Key(asset.id.toString()),
      direction: DismissDirection.endToStart,
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 16),
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      onDismissed: (_) => _deleteAsset(asset.id!),
      child: ListTile(
        leading: CircleAvatar(
          child: Text(asset.assetTypeIcon),
        ),
        title: Text(asset.name),
        subtitle: Text(asset.assetTypeDisplay),
        trailing: Text(
          '¥${asset.value.toStringAsFixed(2)}',
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  void _showAddAssetDialog() {
    showDialog(
      context: context,
      builder: (context) => const AddAssetDialog(),
    );
  }
}

class AddAssetDialog extends StatefulWidget {
  const AddAssetDialog({super.key});

  @override
  State<AddAssetDialog> createState() => _AddAssetDialogState();
}

class _AddAssetDialogState extends State<AddAssetDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _valueController = TextEditingController();

  String _assetType = 'cash';
  bool _isSubmitting = false;

  final List<Map<String, String>> _assetTypes = [
    {'value': 'cash', 'label': '现金'},
    {'value': 'bank_deposit', 'label': '银行存款'},
    {'value': 'fund_etf_stock', 'label': '基金/股票'},
    {'value': 'property', 'label': '房产'},
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

    final asset = Asset(
      name: _nameController.text,
      assetType: _assetType,
      value: double.parse(_valueController.text),
    );

    final success = await context.read<DataProvider>().createAsset(asset);

    if (mounted) {
      setState(() => _isSubmitting = false);

      if (success) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('资产已添加')),
        );
      } else {
        final error = context.read<DataProvider>().assetsError;
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
      title: const Text('添加资产'),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(labelText: '资产名称'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入资产名称';
                  }
                  return null;
                },
              ),
              DropdownButtonFormField<String>(
                value: _assetType,
                decoration: const InputDecoration(labelText: '资产类型'),
                items: _assetTypes.map((type) {
                  return DropdownMenuItem(
                    value: type['value'],
                    child: Text(type['label']!),
                  );
                }).toList(),
                onChanged: (value) => setState(() => _assetType = value!),
              ),
              TextFormField(
                controller: _valueController,
                decoration: const InputDecoration(
                  labelText: '当前价值',
                  prefixText: '¥',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入价值';
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
