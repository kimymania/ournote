import 'dart:io';
import 'package:path_provider/path_provider.dart';

class LocalStorage {
  Future<String> get _localPath async {
    final directory = await getApplicationDocumentsDirectory();
    return directory.path;
  }

  Future<File> writeFile(String roomID, int itemID, String content) async {
    final directory = await _localPath;
    final file = File('$directory/$roomID/$itemID.md');
    return file.writeAsString(content);
  }

  Future<String> readFile(String roomID, int itemID) async {
    final directory = await _localPath;
    final file = File('$directory/$roomID/$itemID.md');
    final contents = await file.readAsString();
    return contents;
  }
}
