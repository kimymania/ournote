import 'package:flutter/material.dart';

class ItemView extends StatefulWidget {
  final String title;
  final String content;
  const ItemView({super.key, required this.title, required this.content});

  @override
  State<ItemView> createState() => _ItemViewState();
}

class _ItemViewState extends State<ItemView> {
  @override
  Widget build(BuildContext context) {
    final titleController = TextEditingController(text: widget.title);
    final contentController = TextEditingController(text: widget.content);

    return Scaffold(
      appBar: AppBar(),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          mainAxisAlignment: .start,
          crossAxisAlignment: .start,
          children: [
            Row(
              mainAxisAlignment: .center,
              crossAxisAlignment: .start,
              spacing: 8,
              children: [
                Expanded(
                  child: TextField(
                    controller: titleController,
                    style: TextStyle(fontSize: 20, fontWeight: .bold),
                    decoration: InputDecoration(border: .none),
                  ),
                ),
              ],
            ),
            Expanded(
              child: TextField(
                controller: contentController,
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
