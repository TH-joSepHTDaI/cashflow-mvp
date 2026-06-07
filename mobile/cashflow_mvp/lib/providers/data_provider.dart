import 'package:flutter/material.dart';
import '../models/transaction.dart';
import '../models/asset.dart';
import '../models/liability.dart';
import '../services/api_service.dart';

/// Loading state for a specific data type
class LoadingState {
  final bool isLoading;
  final String? errorMessage;

  const LoadingState({this.isLoading = false, this.errorMessage});

  LoadingState copyWith({bool? isLoading, String? errorMessage}) {
    return LoadingState(
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
    );
  }

  bool get hasError => errorMessage != null;
}

class DataProvider extends ChangeNotifier {
  // Data storage
  List<Transaction> transactions = [];
  List<Asset> assets = [];
  List<Liability> liabilities = [];

  // Loading states
  LoadingState _transactionsState = const LoadingState();
  LoadingState _assetsState = const LoadingState();
  LoadingState _liabilitiesState = const LoadingState();

  // Getters for loading states
  LoadingState get transactionsState => _transactionsState;
  LoadingState get assetsState => _assetsState;
  LoadingState get liabilitiesState => _liabilitiesState;

  // Backward compatibility getters
  bool get isLoadingTransactions => _transactionsState.isLoading;
  bool get isLoadingAssets => _assetsState.isLoading;
  bool get isLoadingLiabilities => _liabilitiesState.isLoading;
  String? get transactionsError => _transactionsState.errorMessage;
  String? get assetsError => _assetsState.errorMessage;
  String? get liabilitiesError => _liabilitiesState.errorMessage;

  /// Generic method to handle API calls with loading state management
  Future<T?> _handleApiCall<T>({
    required Future<T> Function() apiCall,
    required LoadingState Function() getState,
    required void Function(LoadingState state) setState,
    required void Function(T data) onSuccess,
    String? successMessage,
    BuildContext? context,
  }) async {
    // Set loading state
    setState(getState().copyWith(isLoading: true, errorMessage: null));
    notifyListeners();

    try {
      final result = await apiCall();
      onSuccess(result);
      setState(getState().copyWith(isLoading: false, errorMessage: null));
      notifyListeners();
      return result;
    } on ApiException catch (e) {
      setState(getState().copyWith(isLoading: false, errorMessage: e.message));
      notifyListeners();
      return null;
    } catch (e) {
      // Handle unexpected errors
      final errorMessage = '请求失败，请重试';
      setState(getState().copyWith(isLoading: false, errorMessage: errorMessage));
      notifyListeners();
      return null;
    }
  }

  // ==================== Transactions ====================

  Future<void> loadTransactions({String? month}) async {
    await _handleApiCall<List<Transaction>>(
      apiCall: () => ApiService.getTransactions(month: month),
      getState: () => _transactionsState,
      setState: (state) => _transactionsState = state,
      onSuccess: (data) => transactions = data,
    );
  }

  Future<bool> createTransaction(Transaction transaction) async {
    final result = await _handleApiCall<Transaction>(
      apiCall: () => ApiService.createTransaction(transaction),
      getState: () => _transactionsState,
      setState: (state) => _transactionsState = state,
      onSuccess: (_) {},
    );

    if (result != null) {
      await loadTransactions();
      return true;
    }
    return false;
  }

  Future<bool> deleteTransaction(int id) async {
    await _handleApiCall<void>(
      apiCall: () => ApiService.deleteTransaction(id),
      getState: () => _transactionsState,
      setState: (state) => _transactionsState = state,
      onSuccess: (_) {},
    );

    if (!_transactionsState.hasError) {
      await loadTransactions();
      return true;
    }
    return false;
  }

  // ==================== Assets ====================

  Future<void> loadAssets() async {
    await _handleApiCall<List<Asset>>(
      apiCall: () => ApiService.getAssets(),
      getState: () => _assetsState,
      setState: (state) => _assetsState = state,
      onSuccess: (data) => assets = data,
    );
  }

  Future<bool> createAsset(Asset asset) async {
    final result = await _handleApiCall<Asset>(
      apiCall: () => ApiService.createAsset(asset),
      getState: () => _assetsState,
      setState: (state) => _assetsState = state,
      onSuccess: (_) {},
    );

    if (result != null) {
      await loadAssets();
      return true;
    }
    return false;
  }

  Future<bool> deleteAsset(int id) async {
    await _handleApiCall<void>(
      apiCall: () => ApiService.deleteAsset(id),
      getState: () => _assetsState,
      setState: (state) => _assetsState = state,
      onSuccess: (_) {},
    );

    if (!_assetsState.hasError) {
      await loadAssets();
      return true;
    }
    return false;
  }

  // ==================== Liabilities ====================

  Future<void> loadLiabilities() async {
    await _handleApiCall<List<Liability>>(
      apiCall: () => ApiService.getLiabilities(),
      getState: () => _liabilitiesState,
      setState: (state) => _liabilitiesState = state,
      onSuccess: (data) => liabilities = data,
    );
  }

  Future<bool> createLiability(Liability liability) async {
    final result = await _handleApiCall<Liability>(
      apiCall: () => ApiService.createLiability(liability),
      getState: () => _liabilitiesState,
      setState: (state) => _liabilitiesState = state,
      onSuccess: (_) {},
    );

    if (result != null) {
      await loadLiabilities();
      return true;
    }
    return false;
  }

  Future<bool> deleteLiability(int id) async {
    await _handleApiCall<void>(
      apiCall: () => ApiService.deleteLiability(id),
      getState: () => _liabilitiesState,
      setState: (state) => _liabilitiesState = state,
      onSuccess: (_) {},
    );

    if (!_liabilitiesState.hasError) {
      await loadLiabilities();
      return true;
    }
    return false;
  }

  // ==================== Computed Properties ====================

  double get totalAssetsValue {
    return assets.fold(0, (sum, asset) => sum + asset.value);
  }

  double get totalLiabilitiesValue {
    return liabilities.fold(0, (sum, liability) => sum + liability.value);
  }

  double get netWorth {
    return totalAssetsValue - totalLiabilitiesValue;
  }
}
