from wcferry import Wcf, WxMsg
from queue import Empty
from threading import Thread
from datetime import datetime
import os
import logging
import scheduler  # 导入定时发送消息模块

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Wcf类的实例，用于与微信通信
wcf = Wcf()
logging.info(f"是否已登录: {wcf.is_login()}")
logging.info(f"登录信息: {wcf.get_user_info()}")

contacts = wcf.get_contacts()  # 获取通讯录信息

def send_text_message(msg: str, receiver: str, aters: str = '') -> int:
    """
    发送文本消息
    """
    return wcf.send_text(msg, receiver, aters)

def get_room_name_by_id(room_id):
    """
    根据room_id获取群聊名称
    """
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
            send_text_message(f"这是自动回复的消息\n机器人源码请查看天明的GitHub仓库：https://github.com/ztm0929/Personal-WeChat-Bot\n@{msg.sender} ", room_id, msg.sender)

def enableReceivingMsg():
    """
    启用消息接收功能并启动一个新线程来处理接收到的消息。
    """
    def innerWcFerryProcessMsg():
        """
        内部函数，用于在独立线程中循环处理接收到的消息。
        """
        scheduler.start_scheduler(send_text_message)  # 启动定时任务调度器

        while wcf.is_receiving_msg():  # 判断是否正在接收消息
            try:
                msg = wcf.get_msg()  # 获取接收到的消息
                processMsg(msg)  # 处理消息
            except Empty:  # 处理消息队列为空的情况
                continue  # 继续下一次循环
            except Exception as e:  # 捕获其他所有异常
                logging.error(f"Error: {e}")  # 打印异常信息

    wcf.enable_receiving_msg()  # 启用Wcf实例的消息接收功能
    Thread(target=innerWcFerryProcessMsg, name="ListenMessageThread", daemon=True).start()  # 启动一个后台线程来处理消息

# 启用消息接收功能并启动消息处理线程
enableReceivingMsg()

# 保持Wcf实例的运行状态，使其持续接收消息
wcf.keep_running()
