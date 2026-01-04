import 'package:flutter/material.dart';
import 'package:ournote/models.dart';
import 'package:ournote/service.dart';
import 'package:ournote/views/room.dart';

final apiService = ApiService();

class UserView extends StatefulWidget {
  final String accessToken;
  final String username;
  const UserView({super.key, required this.accessToken, required this.username});

  @override
  State<UserView> createState() => _UserViewState();
}

class _UserViewState extends State<UserView> {
  final _roomPWController = TextEditingController();

  Future<List<Room>> _getRoomsList() async {
    final RoomsList result = await apiService.fetchRoomsList(
      widget.username,
      widget.accessToken,
    );
    final List<Room> roomsList = result.list;
    return roomsList;
  }

  Widget _enterRoom(String roomID) {
    return RoomView(token: widget.accessToken, roomID: roomID);
  }

  String? newRoomID;

  Future<String> _generateRoomID() async {
    final String id = await apiService.generateRoomID();
    setState(() {
      newRoomID = id;
    });
    return id;
  }

  Future<void> _handleRoomCreation() async {
    await apiService.createNewRoom(
      newRoomID!,
      _roomPWController.text,
      widget.accessToken,
    );
    if (!mounted) return;
    Navigator.of(context).pop();
  }

  @override
  void dispose() {
    _roomPWController.dispose();
    super.dispose();
  }

  Future<void> _createNewRoom(BuildContext context) async {
    return showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          title: const Text('Create New Room'),
          content: Column(
            mainAxisAlignment: .center,
            spacing: 8,
            children: [
              Row(
                mainAxisAlignment: .center,
                spacing: 20,
                children: [
                  Container(
                    height: 40,
                    width: 80,
                    alignment: .centerRight,
                    child: Text('Room ID:', textAlign: .center),
                  ),
                  Container(
                    height: 40,
                    width: 100,
                    alignment: .centerLeft,
                    child: FutureBuilder<String>(
                      future: _generateRoomID(),
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
                        } else {
                          return Text('Generating...', textAlign: .center);
                        }
                      },
                    ),
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: .center,
                spacing: 20,
                children: [
                  Container(
                    height: 40,
                    width: 80,
                    alignment: .centerRight,
                    child: Text('PIN:', textAlign: .center),
                  ),
                  Container(
                    height: 40,
                    width: 100,
                    alignment: .centerLeft,
                    child: TextFormField(
                      validator: (String? value) {
                        return value!.isEmpty ? "Enter a PIN number" : null;
                      },
                      controller: _roomPWController,
                      decoration: InputDecoration.collapsed(
                        hintText: '4-digit PIN',
                        hintMaxLines: 1,
                        border: .none,
                      ),
                      obscureText: true,
                    ),
                  ),
                ],
              ),
            ],
          ),
          actions: [
            TextButton(
              child: const Text('OK', textAlign: .end),
              onPressed: () => _handleRoomCreation(),
            ),
            TextButton(
              child: const Text('Cancel', textAlign: .end),
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
          constraints: .tightFor(height: 270, width: 400),
        );
      },
    ).then((value) {
      if (!mounted) return;
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard', style: TextStyle(fontWeight: .bold)),
        centerTitle: false,
        actions: [
          IconButton(
            onPressed: () => _createNewRoom(context),
            icon: const Icon(Icons.add),
          ),
        ],
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
                } else if (snapshot.hasData) {
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      String roomID = snapshot.data![index].id;
                      return ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => _enterRoom(roomID)),
                          );
                        },
                        child: Text(
                          roomID,
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
