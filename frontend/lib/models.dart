import 'dart:convert';

class Result {
  final bool success;
  final String detail;
  final dynamic data;

  const Result({required this.success, required this.detail, this.data = Null});

  factory Result.fromJson(Map<String, dynamic> json) {
    return Result(
      success: json['success'] as bool,
      detail: json['detail'] as String,
      data: json['data'] as dynamic,
    );
  }
}
