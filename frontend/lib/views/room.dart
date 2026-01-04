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
  Future<List<Item>> _handleItemsList() async {
    final ItemsList result = await apiService.fetchItemsList(widget.roomID, widget.token);
    final List<Item> itemList = result.list;
    return itemList;
  }

  void _viewItem(int itemID) async {
    String roomID = widget.roomID;
    final Result result = await apiService.fetch(
      'room/$roomID/item/$itemID',
      widget.token,
    );
    final Item item = Item.fromJson(result.data);

    if (!mounted) return;
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ItemView(
          roomID: roomID,
          itemID: item.id,
          title: item.title,
          content: item.content,
          newItem: false,
        ),
      ),
    ).then((value) {
      if (!mounted) return;
      setState(() {});
    });
  }

  void _addNewItem() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) =>
            ItemView(roomID: widget.roomID, title: 'New Item', content: ''),
      ),
    ).then((value) {
      if (!mounted) return;
      setState(() {});
    });
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
              future: _handleItemsList(),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return Center(child: Text("$snapshot.error"));
                } else if (snapshot.hasData) {
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      int itemID = snapshot.data![index].id;
                      String itemTitle = snapshot.data![index].title;
                      return ElevatedButton(
                        onPressed: () => _viewItem(itemID),
                        child: Text(
                          itemTitle,
                          style: TextStyle(
                            color: Color(0xFF1C1C1C),
                            fontSize: 20,
                            fontWeight: .bold,
                          ),
                        ),
                      );
                    },
                    scrollDirection: .vertical,
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
