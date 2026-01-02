class Result {
  final bool success;
  final String detail;
  final dynamic data;

  const Result({required this.success, required this.detail, this.data = Null});

  factory Result.fromJson(Map<String, dynamic> json) {
    return Result(
      success: json['success'] as bool,
      detail: json['detail'] as String,
      data: json['data'] as dynamic,
    );
  }
}

class Room {
  final String id;

  const Room({required this.id});
}

class RoomsList {
  final List<Room> list;

  const RoomsList({required this.list});

  factory RoomsList.fromJson(Map<String, dynamic> json) {
    List<Room> roomsList = [];
    for (Map<String, String> data in json['rooms']) {
      Room room = Room(id: data['id']!);
      roomsList.add(room);
    }
    return RoomsList(list: roomsList);
  }
}

class Items {
  final String id;
  final String title;
  final String? content;

  const Items({required this.id, required this.title, this.content});

  factory Items.from(Result result) {
    return Items(
      id: result.data['id'] as String,
      title: result.data['title'] as String,
      content: result.data['content'] as String,
    );
  }
}
