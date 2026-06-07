import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/transaction.dart';
import '../models/asset.dart';
import '../models/liability.dart';

/// Custom exception for API errors with user-friendly messages
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final bool isRetryable;

  ApiException({
    required this.message,
    this.statusCode,
    this.isRetryable = false,
  });

  @override
  String toString() => message;
}

/// API Result wrapper for type-safe responses
class ApiResult<T> {
  final T? data;
  final String? errorMessage;
  final bool isSuccess;

  ApiResult._({this.data, this.errorMessage, required this.isSuccess});

  factory ApiResult.success(T data) =>
      ApiResult._(data: data, isSuccess: true);

  factory ApiResult.error(String message) =>
      ApiResult._(errorMessage: message, isSuccess: false);

  bool get hasError => !isSuccess;
}

class ApiService {
  // Change this to your backend URL
  // For Android emulator: use 'http://10.0.2.2:8000'
  // For iOS simulator: use 'http://localhost:8000'
  // For physical device: use your computer's IP address
  static const String baseUrl = 'http://localhost:8000';

  // Timeout configuration
  static const Duration timeoutDuration = Duration(seconds: 10);

  // Retry configuration
  static const int maxRetries = 2;

  /// Standardized error message mapping
  static String _getErrorMessage(int? statusCode, dynamic error) {
    if (error is SocketException || error is TimeoutException) {
      return '无网络连接';
    }
    if (error is TimeoutException) {
      return '连接超时，请检查网络';
    }

    switch (statusCode) {
      case 404:
        return '资源不存在';
      case 500:
      case 502:
      case 503:
      case 504:
        return '服务器错误，请稍后重试';
      case 401:
        return '未授权，请重新登录';
      case 403:
        return '无权限访问';
      case 408:
        return '连接超时，请检查网络';
      case null:
        return '无网络连接';
      default:
        return '请求失败，请重试';
    }
  }

  /// Check if error is retryable (network-related)
  static bool _isRetryableError(dynamic error, int? statusCode) {
    if (error is SocketException) return true;
    if (error is TimeoutException) return true;
    if (error is http.ClientException) return true;
    if (statusCode == 503 || statusCode == 504 || statusCode == 502) return true;
    return false;
  }

  /// Execute HTTP request with timeout and retry logic
  static Future<http.Response> _executeWithRetry(
    Future<http.Response> Function() request, {
    int retries = maxRetries,
  }) async {
    int attempts = 0;
    dynamic lastError;
    int? lastStatusCode;

    while (attempts <= retries) {
      try {
        final response = await request().timeout(timeoutDuration);
        return response;
      } catch (e) {
        lastError = e;
        attempts++;

        // Check if we should retry
        if (attempts <= retries && _isRetryableError(e, null)) {
          // Wait before retry (exponential backoff: 500ms, 1000ms)
          await Future.delayed(Duration(milliseconds: 500 * attempts));
          continue;
        }

        // Don't retry for non-network errors
        if (!_isRetryableError(e, null)) {
          break;
        }
      }
    }

    // Throw standardized exception
    throw ApiException(
      message: _getErrorMessage(lastStatusCode, lastError),
      statusCode: lastStatusCode,
      isRetryable: _isRetryableError(lastError, lastStatusCode),
    );
  }

  /// Handle HTTP response and throw standardized exceptions
  static void _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return;
    }

    throw ApiException(
      message: _getErrorMessage(response.statusCode, null),
      statusCode: response.statusCode,
      isRetryable: response.statusCode >= 500 || response.statusCode == 408,
    );
  }

  // ==================== Transactions ====================

  static Future<List<Transaction>> getTransactions({String? month}) async {
    final url = month != null
        ? '$baseUrl/api/v1/transactions/?month=$month'
        : '$baseUrl/api/v1/transactions/';

    final response = await _executeWithRetry(
      () => http.get(Uri.parse(url)),
    );

    _handleResponse(response);

    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => Transaction.fromJson(json)).toList();
  }

  static Future<Transaction> createTransaction(Transaction transaction) async {
    final response = await _executeWithRetry(
      () => http.post(
        Uri.parse('$baseUrl/api/v1/transactions/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(transaction.toJson()),
      ),
    );

    _handleResponse(response);

    return Transaction.fromJson(json.decode(response.body));
  }

  static Future<void> deleteTransaction(int id) async {
    final response = await _executeWithRetry(
      () => http.delete(Uri.parse('$baseUrl/api/v1/transactions/$id')),
    );

    _handleResponse(response);
  }

  // ==================== Assets ====================

  static Future<List<Asset>> getAssets() async {
    final response = await _executeWithRetry(
      () => http.get(Uri.parse('$baseUrl/api/v1/assets/')),
    );

    _handleResponse(response);

    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => Asset.fromJson(json)).toList();
  }

  static Future<Asset> createAsset(Asset asset) async {
    final response = await _executeWithRetry(
      () => http.post(
        Uri.parse('$baseUrl/api/v1/assets/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(asset.toJson()),
      ),
    );

    _handleResponse(response);

    return Asset.fromJson(json.decode(response.body));
  }

  static Future<void> deleteAsset(int id) async {
    final response = await _executeWithRetry(
      () => http.delete(Uri.parse('$baseUrl/api/v1/assets/$id')),
    );

    _handleResponse(response);
  }

  // ==================== Liabilities ====================

  static Future<List<Liability>> getLiabilities() async {
    final response = await _executeWithRetry(
      () => http.get(Uri.parse('$baseUrl/api/v1/liabilities/')),
    );

    _handleResponse(response);

    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => Liability.fromJson(json)).toList();
  }

  static Future<Liability> createLiability(Liability liability) async {
    final response = await _executeWithRetry(
      () => http.post(
        Uri.parse('$baseUrl/api/v1/liabilities/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(liability.toJson()),
      ),
    );

    _handleResponse(response);

    return Liability.fromJson(json.decode(response.body));
  }

  static Future<void> deleteLiability(int id) async {
    final response = await _executeWithRetry(
      () => http.delete(Uri.parse('$baseUrl/api/v1/liabilities/$id')),
    );

    _handleResponse(response);
  }

  // ==================== Summary Endpoints ====================

  static Future<Map<String, dynamic>> getBalanceSheet() async {
    final response = await _executeWithRetry(
      () => http.get(Uri.parse('$baseUrl/api/v1/balance-sheet/summary')),
    );

    _handleResponse(response);

    return json.decode(response.body);
  }

  static Future<Map<String, dynamic>> getMonthlyCashflow(String month) async {
    final response = await _executeWithRetry(
      () => http.get(
        Uri.parse('$baseUrl/api/v1/cashflow/summary?month=$month'),
      ),
    );

    _handleResponse(response);

    return json.decode(response.body);
  }

  // ==================== Health Check ====================

  static Future<bool> checkHealth() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(const Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
