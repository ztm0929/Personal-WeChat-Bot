import json
import time
import types
import threading
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
import asyncio
import aiohttp
from wcferry import WxMsg, Wcf
from datetime import datetime
import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()


wcf = Wcf()

def send_text_message(msg: str, receiver: str, aters: str = '') -> int:
    return wcf.send_text(msg, receiver, aters)

def get_room_name_by_id(room_id):
    contacts = wcf.get_contacts()
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

def process_msg(msg: WxMsg):
    if msg.from_group():
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
            handle_at_message(msg, room_id, sender_name)

def handle_at_message(msg: WxMsg, room_id: str, sender_name: str):
    def make_request(question: str):
        try:
            start_time = time.time()
            cred = credential.Credential(os.getenv('SecretId'), os.getenv('SecretKey'))
            httpProfile = HttpProfile()
            httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = hunyuan_client.HunyuanClient(cred, "", clientProfile)
            req = models.ChatCompletionsRequest()
            params = {
                "Model": "hunyuan-standard",
                "Messages": [
                    {
                        "Role": "system",
                        "Content": "你是一个编程方面的专家，专门回答编程相关的问题。所有回答以纯文本的方式输出，不要用Markdown或者其他富文本格式。"
                    },
                    {
                        "Role": "user",
                        "Content": question
                    }
                ],
                "Stream": False
            }
            req.from_json_string(json.dumps(params))
            resp = client.ChatCompletions(req)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if isinstance(resp, types.GeneratorType):
                for event in resp:
                    print(event)
            else:
                result = resp.to_json_string()
                result_dict = json.loads(result)
                ai_response = result_dict["Choices"][0]["Message"]["Content"]
                send_text_message(
                    msg=f"@{sender_name} {ai_response}\n\nAI会犯错，最终解释权归@天明所有\n本次请求模型：hunyuan-standard\n本次请求耗时: {elapsed_time:.2f} 秒",
                    receiver=room_id,
                    aters=msg.sender
                )
            print(f"本次请求耗费的时间: {elapsed_time:.2f} 秒")
        except TencentCloudSDKException as err:
            logging.error(f"AI请求失败: {err}")

    question = msg.content.replace(f"@{wcf.get_user_info()['wxid']}", "").strip()
    request_thread = threading.Thread(target=make_request, args=(question,))
    request_thread.start()

def start_scheduler():
    import modules.scheduler
    modules.scheduler.start_scheduler(send_text_message)

def get_wcf_instance():
    return wcf
