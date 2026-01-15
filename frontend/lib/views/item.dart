import 'package:flutter/material.dart';
import 'package:flutter_quill/flutter_quill.dart';
import 'package:ournote/service.dart';

ApiService apiService = ApiService();

class ItemView extends StatefulWidget {
  final String roomID;
  final int? itemID;
  final String title;
  // final String? content;
  final List contentJson;
  final bool newItem;
  const ItemView({
    super.key,
    required this.roomID,
    this.itemID,
    required this.title,
    // required this.content,
    required this.contentJson,
    this.newItem = true,
  });

  @override
  State<ItemView> createState() => _ItemViewState();
}

class _ItemViewState extends State<ItemView> {
  late final _titleController = TextEditingController(text: widget.title);
  late final QuillController _controller = QuillController.basic();
  final toolbarConfig = const QuillSimpleToolbarConfig(
    multiRowsDisplay: false,
    showDividers: false,
    showFontFamily: false,
    showFontSize: false,
    showStrikeThrough: false,
    showInlineCode: false,
    showColorButton: false,
    showBackgroundColorButton: false,
    showClearFormat: false,
    showAlignmentButtons: false,
    showLeftAlignment: false,
    showCenterAlignment: false,
    showRightAlignment: false,
    showJustifyAlignment: false,
    showCodeBlock: false,
    showLink: false,
    showUndo: false,
    showRedo: false,
    showSearchButton: false,
    showSubscript: false,
    showSuperscript: false,
  );

  @override
  void initState() {
    super.initState();
    if (widget.contentJson.isNotEmpty) {
      _controller.document = Document.fromJson(widget.contentJson);
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _controller.dispose();
    super.dispose();
  }

  void _saveNewItem() {
    String title = _titleController.text;
    List<Map<String, dynamic>> contentJson = _controller.document.toDelta().toJson();
    apiService.createNewItem(widget.roomID, title, contentJson);
  }

  void _updateItem() {
    String title = _titleController.text;
    List<Map<String, dynamic>> contentJson = _controller.document.toDelta().toJson();
    apiService.updateItem(widget.roomID, widget.itemID!, title, contentJson);
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
          IconButton(icon: const Icon(Icons.undo), onPressed: () => _controller.undo()),
          IconButton(icon: const Icon(Icons.redo), onPressed: () => _controller.redo()),
          IconButton(
            onPressed: () {
              widget.newItem ? _saveNewItem() : _updateItem();
              Navigator.pop(context);
            },
            icon: const Icon(Icons.check),
          ),
        ],
      ),
      body: SafeArea(
        minimum: const EdgeInsets.symmetric(horizontal: 8.0),
        child: Column(
          children: [
            QuillSimpleToolbar(controller: _controller, config: toolbarConfig),
            Expanded(
              child: QuillEditor.basic(
                controller: _controller,
                config: const QuillEditorConfig(
                  padding: EdgeInsets.symmetric(horizontal: 16.0),
                  autoFocus: true,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
