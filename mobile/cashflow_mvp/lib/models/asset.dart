class Asset {
  final int? id;
  final String name;
  final String assetType;
  final double value;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Asset({
    this.id,
    required this.name,
    required this.assetType,
    required this.value,
    this.createdAt,
    this.updatedAt,
  });

  factory Asset.fromJson(Map<String, dynamic> json) {
    return Asset(
      id: json['id'],
      name: json['name'],
      assetType: json['asset_type'],
      value: json['value'].toDouble(),
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
      updatedAt: json['updated_at'] != null 
          ? DateTime.parse(json['updated_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'asset_type': assetType,
      'value': value,
    };
  }

  String get assetTypeDisplay {
    switch (assetType) {
      case 'cash':
        return '现金';
      case 'bank_deposit':
        return '银行存款';
      case 'fund_etf_stock':
        return '基金/股票';
      case 'property':
        return '房产';
      default:
        return '其他';
    }
  }

  String get assetTypeIcon {
    switch (assetType) {
      case 'cash':
        return '💵';
      case 'bank_deposit':
        return '🏦';
      case 'fund_etf_stock':
        return '📊';
      case 'property':
        return '🏠';
      default:
        return '📦';
    }
  }
}
