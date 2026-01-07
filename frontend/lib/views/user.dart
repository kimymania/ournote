import 'package:flutter/material.dart';
import 'package:ournote/globals.dart';
import 'package:ournote/models.dart';
import 'package:ournote/service.dart';
import 'package:ournote/views/room.dart';

class UserView extends StatefulWidget {
  final Token token;
  final String username;
  const UserView({super.key, required this.token, required this.username});

  @override
  State<UserView> createState() => _UserViewState();
}

class _UserViewState extends State<UserView> {
  final apiService = ApiService();

  Future<List<Room>> _getRoomsList() async {
    return await apiService.fetchRoomsList(widget.username, widget.token);
  }

  // if room is deleted in room view, delete = true
  // this will trigger setState(() {}) for redraw
  Future<bool?> _handleRoomView(String roomID) async {
    bool? delete = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) {
          return RoomView(token: widget.token, roomID: roomID);
        },
      ),
    );
    return delete ?? false;
  }

  void _showCreateDialog() async {
    final bool? success = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (_) => CreateRoomDialog(apiService: apiService, token: widget.token),
    );

    if (success == true) {
      setState(() {});
    }
  }

  Future<bool> _showLeaveDialog(Room room) async {
    final bool? success = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (_) => LeaveRoomDialog(
        apiService: apiService,
        room: room,
        username: widget.username,
        token: widget.token,
      ),
    );
    return success ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: userScaffoldKey,
      appBar: AppBar(
        title: const Text("Dashboard", style: TextStyle(fontWeight: .bold)),
        centerTitle: false,
        actions: [
          IconButton(onPressed: () => _showCreateDialog(), icon: const Icon(Icons.add)),
          IconButton(
            onPressed: () {
              userScaffoldKey.currentState?.openEndDrawer();
            },
            icon: const Icon(Icons.menu),
          ),
        ],
      ),
      endDrawer: Drawer(
        width: 200,
        child: ListView(
          children: [
            DrawerHeader(child: const Text("Settings")),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text("Log Out"),
              onTap: () => redirectToLoginPage(),
            ),
            ListTile(
              leading: const Icon(Icons.delete),
              title: const Text("Delete user", style: TextStyle(color: Colors.red)),
              onTap: () async {
                // TODO: Connect to delete user api
              },
            ),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8.0),
        child: Column(
          mainAxisAlignment: .start,
          crossAxisAlignment: .center,
          children: [
            FutureBuilder(
              future: _getRoomsList(),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return Center(child: Text("$snapshot.error"));
                } else if (snapshot.hasData && snapshot.data!.isEmpty) {
                  return Card(
                    clipBehavior: .hardEdge,
                    child: InkWell(
                      splashColor: Colors.green.withAlpha(30),
                      onTap: () => _showCreateDialog(),
                      child: SizedBox(
                        height: 80,
                        width: double.infinity,
                        child: Center(
                          child: Column(
                            mainAxisAlignment: .center,
                            children: [
                              const Icon(Icons.add),
                              const Text(
                                "Create a new room",
                                style: TextStyle(color: Colors.grey, fontStyle: .italic),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  );
                } else if (snapshot.hasData) {
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      String roomID = snapshot.data![index].id;
                      ValueKey<Room> roomKey = ValueKey<Room>(snapshot.data![index]);
                      return Dismissible(
                        key: roomKey,
                        background: Container(
                          color: Colors.red,
                          alignment: .centerRight,
                          padding: const EdgeInsets.only(right: 20),
                          child: const Icon(Icons.remove_circle, color: Colors.white),
                        ),
                        direction: .endToStart,
                        confirmDismiss: (direction) async {
                          return await _showLeaveDialog(roomKey.value);
                        },
                        onDismissed: (direction) {
                          setState(() => snapshot.data!.removeAt(index));
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text("Left room ${roomKey.value.id}")),
                          );
                        },
                        child: Card(
                          clipBehavior: .hardEdge,
                          child: InkWell(
                            splashColor: Colors.green.withAlpha(30),
                            onTap: () async {
                              await _handleRoomView(roomID).then((value) {
                                if (value!) {
                                  setState(() {});
                                }
                              });
                            },
                            child: SizedBox(
                              height: 50,
                              width: double.infinity,
                              child: Center(
                                child: Column(
                                  mainAxisAlignment: .center,
                                  children: [
                                    Text(
                                      roomID,
                                      style: const TextStyle(
                                        color: Color(0xFF1C1C1C),
                                        fontSize: 20,
                                        fontWeight: .bold,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                    scrollDirection: .vertical,
                    shrinkWrap: true,
                  );
                } else {
                  return const SizedBox(
                    width: 15,
                    height: 15,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}

class CreateRoomDialog extends StatefulWidget {
  final ApiService apiService;
  final Token token;

  const CreateRoomDialog({super.key, required this.apiService, required this.token});

  @override
  State<CreateRoomDialog> createState() => _CreateRoomDialogState();
}

class _CreateRoomDialogState extends State<CreateRoomDialog> {
  final _passwordController = TextEditingController();
  late Future<String> roomIdFuture;

  @override
  void initState() {
    super.initState();
    roomIdFuture = widget.apiService.generateRoomID();
  }

  @override
  void dispose() {
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final roomId = await roomIdFuture;
    if (!mounted) return;
    try {
      await widget.apiService.createNewRoom(
        roomId,
        _passwordController.text,
        widget.token,
      );
      if (!mounted) return;
      Navigator.of(context).pop(true);
    } catch (e) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Error! Failed to create room")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text("Create New Room"),
      content: SizedBox(
        height: 100,
        width: 300,
        child: Column(
          children: [
            Row(
              mainAxisAlignment: .spaceBetween,
              spacing: 20,
              children: [
                const Text("Room ID:", textAlign: .center),
                FutureBuilder<String>(
                  future: roomIdFuture,
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      return Text(
                        snapshot.data!,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: .bold,
                          color: Colors.red,
                        ),
                      );
                    }
                    return const SizedBox(
                      width: 15,
                      height: 15,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    );
                  },
                ),
              ],
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: .spaceBetween,
              children: [
                const Text("PIN:"),
                SizedBox(
                  width: 100,
                  child: TextFormField(
                    validator: (String? value) {
                      return value!.isEmpty ? "Enter a PIN number" : null;
                    },
                    controller: _passwordController,
                    decoration: const InputDecoration(
                      hintText: "4-digit PIN",
                      hintMaxLines: 1,
                      border: .none,
                      isDense: true,
                    ),
                    obscureText: true,
                  ),
                ),
              ],
            ),
          ],
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

class LeaveRoomDialog extends StatefulWidget {
  final ApiService apiService;
  final Room room;
  final String username;
  final Token token;

  const LeaveRoomDialog({
    super.key,
    required this.apiService,
    required this.room,
    required this.username,
    required this.token,
  });

  @override
  State<LeaveRoomDialog> createState() => _LeaveRoomDialogState();
}

class _LeaveRoomDialogState extends State<LeaveRoomDialog> {
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    try {
      await widget.apiService.leaveRoom(
        widget.room.id,
        widget.username,
        _passwordController.text,
        widget.token,
      );
      if (!mounted) return;
      Navigator.of(context).pop(true);
    } catch (e) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Error! Failed to leave room")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text("Leave room?"),
      content: SizedBox(
        height: 100,
        width: 300,
        child: TextFormField(
          validator: (String? value) {
            return value!.isEmpty ? "Enter password" : null;
          },
          controller: _passwordController,
          decoration: const InputDecoration(
            labelText: "Enter password",
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
