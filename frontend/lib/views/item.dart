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
      appBar: AppBar(
        title: SizedBox(
          height: kToolbarHeight,
          child: Column(
            mainAxisAlignment: .center,
            crossAxisAlignment: .start,
            children: [
              TextField(
                controller: titleController,
                style: TextStyle(fontSize: 22, fontWeight: .bold),
                decoration: InputDecoration(
                  hintText: 'Title',
                  hintMaxLines: 1,
                  border: .none,
                ),
              ),
            ],
          ),
        ),
        toolbarHeight: kToolbarHeight,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          mainAxisAlignment: .start,
          crossAxisAlignment: .start,
          children: [
            // SizedBox(
            //   height: 80,
            //   width: double.infinity,
            //   child: TextField(
            //     controller: titleController,
            //     style: TextStyle(fontSize: 20, fontWeight: .bold),
            //     decoration: InputDecoration(border: .none),
            //   ),
            // ),
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
