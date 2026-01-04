import 'package:flutter/material.dart';
import 'package:ournote/models.dart';
import 'package:ournote/service.dart';
import 'package:ournote/views/item.dart';

final apiService = ApiService();

class RoomView extends StatefulWidget {
  final String token;
  final String roomID;
  const RoomView({super.key, required this.token, required this.roomID});

  @override
  State<RoomView> createState() => _RoomViewState();
}

class _RoomViewState extends State<RoomView> {
  Future<List<Item>> _handleItems() async {
    final ItemsList result = await apiService.fetchItemsList(widget.roomID, widget.token);
    final List<Item> itemList = result.list;
    return itemList;
  }

  String _getItemContent(String? content) {
    if (content == null) {
      return '';
    } else {
      return content;
    }
  }

  void _addNewItem() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ItemView(title: 'New Item', content: ''),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.roomID, style: TextStyle(fontWeight: .bold)),
        centerTitle: false,
        actions: [
          IconButton(onPressed: () => _addNewItem(), icon: const Icon(Icons.add)),
        ],
        actionsPadding: const EdgeInsets.symmetric(horizontal: 8),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Column(
          mainAxisAlignment: .start,
          crossAxisAlignment: .start,
          spacing: 8,
          children: [
            FutureBuilder(
              future: _handleItems(),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return Center(child: Text("$snapshot.error"));
                } else if (snapshot.hasData) {
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      String buttonValue = snapshot.data![index].title;
                      String itemContent = _getItemContent(snapshot.data![index].content);
                      return ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  ItemView(title: buttonValue, content: itemContent),
                            ),
                          );
                        },
                        child: Text(
                          buttonValue,
                          style: TextStyle(
                            color: Color(0xFF1C1C1C),
                            fontSize: 20,
                            fontWeight: .bold,
                          ),
                        ),
                      );
                    },
                    scrollDirection: Axis.vertical,
                    shrinkWrap: true,
                  );
                } else {
                  return Center(child: Text("Loading..."));
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
