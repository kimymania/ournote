import 'package:flutter/material.dart';
import 'package:ournote/service.dart';

ApiService apiService = ApiService();

class ItemView extends StatefulWidget {
  final String roomID;
  final int? itemID;
  final String title;
  final String? content;
  final bool newItem;
  const ItemView({
    super.key,
    required this.roomID,
    this.itemID,
    required this.title,
    required this.content,
    this.newItem = true,
  });

  @override
  State<ItemView> createState() => _ItemViewState();
}

class _ItemViewState extends State<ItemView> {
  late final _titleController = TextEditingController(text: widget.title);
  late final _contentController = TextEditingController(text: widget.content);

  @override
  void dispose() {
    _titleController.dispose();
    _contentController.dispose();
    super.dispose();
  }

  void _saveNewItem() {
    String title = _titleController.text;
    String content = _contentController.text;
    apiService.createNewItem(widget.roomID, title, content);
  }

  void _updateItem() {
    String title = _titleController.text;
    String content = _contentController.text;
    apiService.updateItem(widget.roomID, widget.itemID!, title, content);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: SizedBox(
          height: kToolbarHeight,
          child: Column(
            mainAxisAlignment: .center,
            crossAxisAlignment: .start,
            children: [
              TextField(
                controller: _titleController,
                style: TextStyle(fontSize: 22, fontWeight: .bold),
                decoration: InputDecoration(
                  hintText: "Title",
                  hintMaxLines: 1,
                  border: .none,
                ),
              ),
            ],
          ),
        ),
        toolbarHeight: kToolbarHeight,
        actions: [
          IconButton(
            onPressed: () {
              widget.newItem ? _saveNewItem() : _updateItem();
              Navigator.pop(context);
            },
            icon: const Icon(Icons.check),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          mainAxisAlignment: .start,
          crossAxisAlignment: .start,
          children: [
            Expanded(
              child: TextField(
                controller: _contentController,
                decoration: InputDecoration.collapsed(
                  hintText: "Enter content...",
                  hintStyle: TextStyle(color: Colors.white70),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
