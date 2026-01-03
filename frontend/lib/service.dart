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

  Future<dynamic> fetch(String path, String token) async {
    final url = Uri.parse('$baseUrl/$path');
    final authHeaders = {'Authorization': 'Bearer $token'};

    final response = await http.get(url, headers: authHeaders);
    try {
      if (response.statusCode != 200) {
        throw HttpException('Failed to load data');
      } else {
        final Result jsonResponse = Result.fromJson(jsonDecode(response.body));
        return jsonResponse;
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<RoomsList> fetchRoomsList(String username, String token) async {
    final url = Uri.parse('$baseUrl/$userUrl/$username');
    final headers = {'Authorization': 'Bearer $token'};

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode != 200) {
        throw HttpException('Failed to load data');
      } else {
        final RoomsList roomsList = RoomsList.fromJson(jsonDecode(response.body));
        return roomsList;
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<ItemsList> fetchItemsList(String roomID, String token) async {
    final url = Uri.parse('$baseUrl/$roomUrl/$roomID');
    final headers = {'Authorization': 'Bearer $token'};

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode != 200) {
        throw HttpException('Failed to load data');
      } else {
        final ItemsList itemsList = ItemsList.fromJson(jsonDecode(response.body));
        return itemsList;
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<String?> getToken(String username, String password) async {
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
