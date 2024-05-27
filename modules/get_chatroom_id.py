from wcferry import Wcf, WxMsg

wcf = Wcf()

wcf_rooms = []

for contact in wcf.get_contacts():
    if contact['wxid'].endswith("chatroom"):
        wcf_rooms.append(contact)

def get_chatroom_roomid(wcf_rooms: list, room_name: str):
    for room in wcf_rooms:
        if room['name'] == room_name:
            return room['wxid']
    return None

room_id = get_chatroom_roomid(wcf_rooms=wcf_rooms, room_name="闲聊区@编程小白社")
print(room_id)