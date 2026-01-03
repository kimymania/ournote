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
    for (Map<String, dynamic> data in json['rooms']) {
      Room room = Room(id: data['id']!);
      roomsList.add(room);
    }
    return RoomsList(list: roomsList);
  }
}

class Item {
  final String title;
  final String? content;

  const Item({required this.title, this.content});
}

class ItemsList {
  final List<Item> list;

  const ItemsList({required this.list});

  factory ItemsList.fromJson(Map<String, dynamic> json) {
    if (json['items'] == null) {
      return ItemsList(list: []);
    }

    List<Item> itemsList = [];
    for (Map<String, dynamic> data in json['items']) {
      Item item = Item(title: data['title']!, content: data['content']);
      itemsList.add(item);
    }
    return ItemsList(list: itemsList);
  }
}
