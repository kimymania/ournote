import 'package:flutter/material.dart';
import 'package:ournote/models.dart';
import 'package:ournote/service.dart';
import 'package:ournote/views/room.dart';

final apiService = ApiService();

class UserView extends StatelessWidget {
  final String accessToken;
  final String username;
  const UserView({super.key, required this.accessToken, required this.username});

  Future<List<Room>> _getRoomsList() async {
    final RoomsList result = await apiService.fetchRoomsList(username, accessToken);
    final List<Room> roomsList = result.list;
    return roomsList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard', style: TextStyle(fontWeight: .bold)),
        centerTitle: false,
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
                      String buttonValue = snapshot.data![index].id;
                      return ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  RoomView(token: accessToken, roomID: buttonValue),
                            ),
                          );
                        },
                        child: Container(
                          padding: EdgeInsets.all(8),
                          decoration: ShapeDecoration(
                            color: Colors.green[50],
                            shape: RoundedSuperellipseBorder(
                              borderRadius: .circular(20),
                              side: BorderSide(color: Color(0xAA1C1C1C)),
                            ),
                          ),
                          height: 80,
                          child: Center(
                            child: Text(
                              buttonValue,
                              style: TextStyle(
                                color: Color(0xFF1C1C1C),
                                fontSize: 20,
                                fontWeight: .bold,
                              ),
                            ),
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
