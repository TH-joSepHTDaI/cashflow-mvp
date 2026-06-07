class Transaction {
  final int? id;
  final double amount;
  final String date;
  final String? note;
  final String category;
  final String cashflowType;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Transaction({
    this.id,
    required this.amount,
    required this.date,
    this.note,
    required this.category,
    required this.cashflowType,
    this.createdAt,
    this.updatedAt,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) {
    return Transaction(
      id: json['id'],
      amount: json['amount'].toDouble(),
      date: json['date'],
      note: json['note'],
      category: json['category'],
      cashflowType: json['cashflow_type'],
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
      'amount': amount,
      'date': date,
      'note': note,
      'category': category,
      'cashflow_type': cashflowType,
    };
  }

  String get cashflowTypeDisplay {
    switch (cashflowType) {
      case 'income':
        return '收入';
      case 'expense':
        return '支出';
      case 'investment':
        return '投资';
      case 'liability_repayment':
        return '负债还款';
      default:
        return '其他';
    }
  }

  String get cashflowTypeIcon {
    switch (cashflowType) {
      case 'income':
        return '↓';
      case 'expense':
        return '↑';
      case 'investment':
        return '📈';
      case 'liability_repayment':
        return '💳';
      default:
        return '•';
    }
  }
}
