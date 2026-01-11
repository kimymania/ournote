import 'package:flutter/material.dart';
import 'package:ournote/globals.dart';
import 'package:ournote/models.dart';
import 'package:ournote/service.dart';
import 'package:ournote/views/item.dart';

final apiService = ApiService();

class RoomView extends StatefulWidget {
  final Token token;
  final String roomID;
  final String roomName;
  const RoomView({
    super.key,
    required this.token,
    required this.roomID,
    required this.roomName,
  });

  @override
  State<RoomView> createState() => _RoomViewState();
}

class _RoomViewState extends State<RoomView> {
  Future<List<Item>> _handleItemsList() async {
    final ItemsList result = await apiService.fetchItemsList(
      widget.roomID,
      widget.token,
    );
    final List<Item> itemList = result.list;
    return itemList;
  }

  void _viewItem(int itemID) async {
    String roomID = widget.roomID;
    final Item item = await apiService.fetchItem(roomID, itemID, widget.token);

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
            ItemView(roomID: widget.roomID, title: "New Item", content: ""),
      ),
    ).then((value) {
      if (!mounted) return;
      setState(() {});
    });
  }

  Future<bool> _showDeleteDialog() async {
    final bool? success = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (_) => DeleteRoomDialog(
        apiService: apiService,
        roomID: widget.roomID,
        token: widget.token,
      ),
    );
    return success ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: roomScaffoldKey,
      appBar: AppBar(
        title: Text(widget.roomName, style: TextStyle(fontWeight: .bold)),
        centerTitle: false,
        actions: [
          IconButton(
            onPressed: () => _addNewItem(),
            icon: const Icon(Icons.create),
          ),
          IconButton(
            onPressed: () {
              roomScaffoldKey.currentState?.openEndDrawer();
            },
            icon: const Icon(Icons.menu),
          ),
        ],
        actionsPadding: const EdgeInsets.symmetric(horizontal: 8),
      ),
      endDrawer: Drawer(
        width: 200,
        child: ListView(
          children: [
            DrawerHeader(child: const Text("Settings")),
            ListTile(
              leading: const Icon(Icons.mail),
              title: const Text("Invite member"),
              // TODO: onTap functionality to generate & send invitation code
            ),
            ListTile(
              leading: const Icon(Icons.delete),
              title: const Text(
                "Delete room",
                style: TextStyle(color: Colors.red),
              ),
              onTap: () async {
                bool result = await _showDeleteDialog();
                if (result) {
                  if (context.mounted) {
                    Navigator.of(context).pop(true);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text("Deleted room ${widget.roomID}")),
                    );
                  }
                }
              },
            ),
          ],
        ),
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
                      return Dismissible(
                        key: ValueKey<Item>(snapshot.data![index]),
                        background: Container(
                          color: Colors.red,
                          child: Icon(Icons.delete, color: Colors.white),
                        ),
                        onDismissed: (direction) {
                          apiService.deleteItem(widget.roomID, itemID);
                          setState(() => snapshot.data!.removeAt(index));
                        },
                        child: ElevatedButton(
                          onPressed: () => _viewItem(itemID),
                          child: Text(
                            itemTitle,
                            style: TextStyle(
                              color: Color(0xFF1C1C1C),
                              fontSize: 20,
                              fontWeight: .bold,
                            ),
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

class DeleteRoomDialog extends StatefulWidget {
  final ApiService apiService;
  final String roomID;
  final Token token;
  const DeleteRoomDialog({
    super.key,
    required this.apiService,
    required this.roomID,
    required this.token,
  });

  @override
  State<DeleteRoomDialog> createState() => _DeleteRoomDialog();
}

class _DeleteRoomDialog extends State<DeleteRoomDialog> {
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    Room room = Room(id: widget.roomID, password: _passwordController.text);
    try {
      await widget.apiService.deleteRoom(room, widget.token);
      if (!mounted) return;
      Navigator.of(context).pop(true);
    } catch (e) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Error! Failed to delete room: ${e.toString()}"),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text("Delete room?"),
      content: SizedBox(
        height: 80,
        width: 300,
        child: TextFormField(
          validator: (String? value) {
            return value!.isEmpty ? "Enter 4-digit PIN" : null;
          },
          controller: _passwordController,
          decoration: const InputDecoration(
            labelText: "Enter Room PIN",
            border: .none,
            isDense: true,
          ),
          obscureText: true,
        ),
      ),
      actions: [
        TextButton(child: const Text("OK"), onPressed: () => _submit()),
        TextButton(
          child: const Text("Cancel"),
          onPressed: () => Navigator.of(context).pop(false),
        ),
      ],
    );
  }
}
