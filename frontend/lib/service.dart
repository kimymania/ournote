import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'models.dart';

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000";
  final String userUrl = "user";
  final String roomUrl = "room";
  final String itemUrl = "item";

  Future<void> send(String name, double price) async {
    final response = await http.post(
      Uri.parse('$baseUrl/items'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'price': price}),
    );

    if (response.statusCode == 200) {
      print("Item created: ${response.body}");
    }
  }

  Future<dynamic> fetch(String path) async {
    final url = Uri.parse('$baseUrl/$path');
    final response = await http.get(url);

    try {
      if (response.statusCode != 200) {
        throw HttpException('Failed to load data');
      } else {
        final dynamic jsonResponse = jsonDecode(response.body);
        return jsonResponse;
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<RoomsList> fetchRoomsList(String username) async {
    final url = Uri.parse('$baseUrl/$userUrl/$username');

    try {
      final response = await http.get(url);
      if (response.statusCode != 200) {
        throw HttpException('Failed to load data');
      } else {
        final RoomsList roomsList = jsonDecode(response.body);
        return roomsList;
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<String?> sendCredentials(String username, String password) async {
    final userData = {'username': username, 'password': password};
    final url = Uri.parse('$baseUrl/token');

    try {
      final response = await http.post(url, body: userData);
      if (response.statusCode != 200) {
        throw Exception('Authentication failed');
      } else {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return jsonResponse['access_token'];
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }
}
