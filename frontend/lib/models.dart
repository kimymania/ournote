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
  final int id;
  final String title;
  final String? content;

  const Item({required this.id, required this.title, this.content});

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'] as int,
      title: json['title'] as String,
      content: json['content'] as String,
    );
  }
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
      Item item = Item(id: data['id'], title: data['title'], content: data['content']);
      itemsList.add(item);
    }
    return ItemsList(list: itemsList);
  }
}
