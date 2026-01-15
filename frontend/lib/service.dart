import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:ournote/globals.dart';
import 'package:ournote/models.dart';
import 'package:ournote/views/login.dart';

void redirectToLoginPage() {
  navigatorKey.currentState?.pushAndRemoveUntil(
    MaterialPageRoute(builder: (context) => LoginPage()),
    (route) => false,
  );
}

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000";

  Future<Token?> getToken(String username, String password) async {
    final url = Uri.parse("$baseUrl/token");
    final body = {"username": username, "password": password};

    try {
      final response = await http.post(url, body: body);
      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        Token token = Token(tokenString: jsonResponse["access_token"]);
        return token;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw Exception("Authentication failed");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> createUser(String username, String password) async {
    final url = Uri.parse("$baseUrl/user/create");
    final body = {"username": username, "password": password};

    try {
      final response = await http.post(url, body: body);
      if (response.statusCode == 201) {
        return;
      } else {
        throw HttpException("Failed to create user");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> deleteUser(String username, String password, Token token) async {
    final url = Uri.parse("$baseUrl/user/$username");
    final tokenHeader = Token.getHeader(token);
    final headers = {
      tokenHeader.keys.first: tokenHeader.values.first,
      "Content-Type": "application/json",
    };
    final body = {"username": username, "password": password};

    try {
      final response = await http.delete(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        return;
      } else {
        throw HttpException("Failed to delete user");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<String> generateRoomID() async {
    final url = Uri.parse("$baseUrl/room_id");

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return jsonResponse["id"];
      } else {
        throw HttpException("Failed to load data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> createNewItem(
    String roomID,
    String title,
    List<Map<String, dynamic>> contentJson,
  ) async {
    try {
      final response = await http.post(
        Uri.parse("$baseUrl/room/$roomID/item/create"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"title": title, "content_json": contentJson}),
      );

      if (response.statusCode == 201) {
        return;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
      } else {
        throw HttpException("Failed to update data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<dynamic> fetchItem(String roomID, int itemID, Token token) async {
    final url = Uri.parse("$baseUrl/room/$roomID/item/$itemID");
    final headers = Token.getHeader(token);

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        final Item item = Item.fromJson(jsonDecode(response.body));
        return item;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw HttpException("Failed to load data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> updateItem(
    String roomID,
    int itemID,
    String title,
    List<Map<String, dynamic>> contentJson,
  ) async {
    try {
      final response = await http.put(
        Uri.parse("$baseUrl/room/$roomID/item/$itemID"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"title": title, "content_json": contentJson}),
      );

      if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
      } else if (response.statusCode != 200) {
        throw HttpException("Failed to update data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> deleteItem(String roomID, int itemID) async {
    try {
      final response = await http.delete(Uri.parse("$baseUrl/room/$roomID/item/$itemID"));

      if (response.statusCode == 200) {
        return;
      } else {
        throw HttpException("Failed to delete data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<List<Room>> fetchRoomsList(String username, Token token) async {
    final url = Uri.parse("$baseUrl/user/$username");
    final headers = Token.getHeader(token);

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        final RoomsList roomsList = RoomsList.fromJson(jsonDecode(response.body));
        final List<Room> parsedList = roomsList.list;
        return parsedList;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw HttpException("Failed to load data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> createNewRoom(
    String roomID,
    String roomName,
    String roomPW,
    Token token,
  ) async {
    final url = Uri.parse("$baseUrl/room/create");
    final headers = Token.getHeader(token);
    final body = {"room_id": roomID, "room_name": roomName, "room_pw": roomPW};

    try {
      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 201) {
        return;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw Exception("Room creation failed");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> editRoomName(String roomID, String newName, Token token) async {
    // TODO: fix 422 error
    final url = Uri.parse("$baseUrl/room/$roomID");
    final tokenHeader = Token.getHeader(token);
    final headers = {"Content-Type": "application/json", ...tokenHeader};
    final body = jsonEncode({"room_name": newName});

    try {
      final response = await http.put(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        return;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw HttpException("Failed to edit name");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<ItemsList> fetchItemsList(String roomID, Token token) async {
    final url = Uri.parse("$baseUrl/room/$roomID");
    final headers = Token.getHeader(token);

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        final ItemsList itemsList = ItemsList.fromJson(jsonDecode(response.body));
        return itemsList;
      } else if (response.statusCode == 401 || response.statusCode == 403) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else {
        throw HttpException("Failed to load data");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> deleteRoom(Room room, Token token) async {
    final roomID = room.id;
    final url = Uri.parse("$baseUrl/room/$roomID");
    final headers = Token.getHeader(token);
    final body = {"room_pw": room.password};

    try {
      final response = await http.delete(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        return;
      } else if (response.statusCode == 401) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else if (response.statusCode == 403) {
        throw Exception("wrong pin number");
      } else {
        int errorCode = response.statusCode;
        throw Exception("errorCode=$errorCode, url=$url, headers=$headers, body=$body");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }

  Future<void> leaveRoom(
    String roomID,
    String username,
    String password,
    Token token,
  ) async {
    final url = Uri.parse("$baseUrl/room/$roomID/$username");
    final headers = Token.getHeader(token);
    final body = {"password": password};

    try {
      final response = await http.delete(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        return;
      } else if (response.statusCode == 401) {
        redirectToLoginPage();
        throw HttpException("Session timed out");
      } else if (response.statusCode == 403) {
        throw Exception("wrong password");
      } else {
        int errorCode = response.statusCode;
        throw Exception("errorCode=$errorCode, url=$url, headers=$headers, body=$body");
      }
    } on SocketException {
      throw Exception("Connection failure");
    }
  }
}
