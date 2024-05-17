# message_processor.py
import asyncio
import aiohttp
from wcferry import WxMsg, Wcf
from datetime import datetime
import os
import logging
import requests

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Wcf类的实例，用于与微信通信
wcf = Wcf()

def send_text_message(msg: str, receiver: str, aters: str = '') -> int:
    """
    发送文本消息
    """
    return wcf.send_text(msg, receiver, aters)

def get_room_name_by_id(room_id):
    """
    根据room_id获取群聊名称
    """
    contacts = wcf.get_contacts()  # 获取通讯录信息
    for contact in contacts:
        if contact['wxid'] == room_id:
            return contact['name']
    return "未知群聊"

def write_message_log(room_name, room_id, msg):
    """
    将消息记录写入日志文件
    """
    log_dir = os.path.join("logs", "chat_logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{room_name}_{room_id}_{datetime.now().strftime('%Y-%m-%d')}.csv")
    
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding='utf-8') as f:
            f.write("msg.id,msg.sender,datetime,msg.content\n")
    
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"{msg.id},{msg.sender},{datetime.now().strftime('%H:%M:%S')},{msg.content}\n")

def processMsg(msg: WxMsg):
    """
    处理微信消息的函数。如果消息来自群聊，打印消息内容。
    """
    if msg.from_group():  # 判断消息是否来自群聊
        room_id = msg.roomid
        room_name = get_room_name_by_id(room_id)
        logging.info(f"来自群聊 {room_name} 的消息：{msg.content}")
        logging.info(f"消息ID：{msg.id},消息发送人：{msg.sender}")

        write_message_log(room_name, room_id, msg)
        
        if msg.is_at(wcf.get_user_info()['wxid']):
            sender_name = wcf.get_alias_in_chatroom(msg.sender, room_id)
            send_text_message(
                msg=f"@{sender_name}\n\n请稍候，我正在查询...",
                receiver=room_id,
                aters=msg.sender
            )
            if "查询" in msg.content:
                send_text_message(
                    msg=requests.get('http://127.0.0.1:5000/repositories').json()[0]['url'],
                    receiver=room_id,
                    aters=msg.sender
                )
                print(requests.get('http://127.0.0.1:5000/repositories').json()[0]['url'])

def start_scheduler():
    import scheduler
    scheduler.start_scheduler(send_text_message)

def get_wcf_instance():
    return wcf
