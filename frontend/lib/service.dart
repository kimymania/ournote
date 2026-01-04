import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:ournote/globals.dart';
import 'package:ournote/models.dart';
import 'package:ournote/views/login.dart';

void _redirectToLoginPage() {
  navigatorKey.currentState?.pushReplacement(
    MaterialPageRoute(builder: (context) => LoginPage()),
  );
}

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000";

  Future<void> saveNewItem(String roomID, String title, String content) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/room/$roomID/item/create'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'title': title, 'content': content}),
      );

      if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
      } else if (response.statusCode != 200) {
        throw HttpException('Failed to update data');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<void> updateItem(String roomID, int itemID, String title, String content) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/room/$roomID/item/$itemID'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'title': title, 'content': content}),
      );

      if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
      } else if (response.statusCode != 200) {
        throw HttpException('Failed to update data');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<dynamic> fetch(String path, String token) async {
    final url = Uri.parse('$baseUrl/$path');
    final authHeaders = {'Authorization': 'Bearer $token'};

    try {
      final response = await http.get(url, headers: authHeaders);
      if (response.statusCode == 200) {
        final Result jsonResponse = Result.fromJson(jsonDecode(response.body));
        return jsonResponse;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
        throw HttpException('Session timed out');
      } else {
        throw HttpException('Failed to load data');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<RoomsList> fetchRoomsList(String username, String token) async {
    final url = Uri.parse('$baseUrl/user/$username');
    final headers = {'Authorization': 'Bearer $token'};

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        final RoomsList roomsList = RoomsList.fromJson(jsonDecode(response.body));
        return roomsList;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
        throw HttpException('Session timed out');
      } else {
        throw HttpException('Failed to load data');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<ItemsList> fetchItemsList(String roomID, String token) async {
    final url = Uri.parse('$baseUrl/room/$roomID');
    final headers = {'Authorization': 'Bearer $token'};

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        final ItemsList itemsList = ItemsList.fromJson(jsonDecode(response.body));
        return itemsList;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
        throw HttpException('Session timed out');
      } else {
        throw HttpException('Failed to load data');
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
      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return jsonResponse['access_token'];
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
        throw HttpException('Session timed out');
      } else {
        throw Exception('Authentication failed');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<String> generateRoomID() async {
    final url = Uri.parse('$baseUrl/room_id');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final Result result = Result.fromJson(jsonDecode(response.body));
        final String id = result.data;
        return id;
      } else {
        throw HttpException('Failed to load data');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }

  Future<void> createNewRoom(String roomID, String roomPW, String token) async {
    final roomData = {'room_id': roomID, 'room_pw': roomPW};
    final headers = {'Authorization': 'Bearer $token'};
    final url = Uri.parse('$baseUrl/room/create');

    try {
      final response = await http.post(url, headers: headers, body: roomData);
      if (response.statusCode == 401 || response.statusCode == 403) {
        _redirectToLoginPage();
        throw HttpException('Session timed out');
      } else if (response.statusCode != 200) {
        throw Exception('Room creation failed');
      }
    } on SocketException {
      throw Exception('Connection failure');
    }
  }
}
