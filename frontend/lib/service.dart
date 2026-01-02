import 'dart:convert';
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

    if (response.statusCode == 200) {
      final dynamic jsonResponse = jsonDecode(response.body);
      return jsonResponse;
    } else {
      throw Exception('Failed to load data');
    }
  }

  Future<RoomsList> fetchRoomsList(String username) async {
    final url = Uri.parse('$baseUrl/$userUrl/$username');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final RoomsList roomsList = jsonDecode(response.body);
      return roomsList;
    } else {
      throw Exception('Failed to load data');
    }
  }

  Future<String?> sendCredentials(String username, String password) async {
    final userData = {'username': username, 'password': password};
    final url = Uri.parse('$baseUrl/token');
    final response = await http.post(url, body: userData);

    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
      return jsonResponse['access_token'];
    } else {
      throw Exception('Authentication failed');
    }
  }
}
