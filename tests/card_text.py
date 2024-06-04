from wcferry import Wcf, WxMsg
from queue import Empty
import logging
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()

wcf = Wcf()

def send_text_message(msg: str, receiver: str, aters: str = '') -> int:
    return wcf.send_text(msg, receiver, aters)

def send_rich_text_message(name: str, account: str, title: str, digest: str, url: str, thumburl: str, receiver: str) -> int:
    return wcf.send_rich_text(name, account, title, digest, url, thumburl, receiver)

def process_msg(msg: WxMsg):
    if msg.from_group():        
        if msg.is_at(wcf.get_user_info()['wxid']):
            send_text_message(
                msg = "测试",
                receiver = os.getenv("测试专用"),
                aters=""
            )
            send_rich_text_message(
                name = "测试",
                account = "",
                title = "测试",
                digest = "",
                url = "www.baidu.com",
                thumburl = "",
                receiver = os.getenv("测试专用")
            )

def enableReceivingMsg():
    def innerWcFerryProcessMsg():
        while wcf.is_receiving_msg():
            try:
                msg = wcf.get_msg()
                process_msg(msg)
            except Empty:
                continue
            except Exception as e:
                logging.error(f"Error: {e}")

    wcf.enable_receiving_msg()
    Thread(target=innerWcFerryProcessMsg, name="ListenMessageThread", daemon=True).start()

enableReceivingMsg()

wcf.keep_running()