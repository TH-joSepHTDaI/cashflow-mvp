class Liability {
  final int? id;
  final String name;
  final String liabilityType;
  final double value;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Liability({
    this.id,
    required this.name,
    required this.liabilityType,
    required this.value,
    this.createdAt,
    this.updatedAt,
  });

  factory Liability.fromJson(Map<String, dynamic> json) {
    return Liability(
      id: json['id'],
      name: json['name'],
      liabilityType: json['liability_type'],
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
      'liability_type': liabilityType,
      'value': value,
    };
  }

  String get liabilityTypeDisplay {
    switch (liabilityType) {
      case 'credit_card':
        return '信用卡';
      case 'mortgage':
        return '房贷';
      case 'car_loan':
        return '车贷';
      case 'consumer_loan':
        return '消费贷';
      default:
        return '其他';
    }
  }

  String get liabilityTypeIcon {
    switch (liabilityType) {
      case 'credit_card':
        return '💳';
      case 'mortgage':
        return '🏠';
      case 'car_loan':
        return '🚗';
      case 'consumer_loan':
        return '💰';
      default:
        return '📋';
    }
  }
}
