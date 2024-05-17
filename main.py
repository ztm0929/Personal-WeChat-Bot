from wcferry import Wcf, WxMsg
from queue import Empty
from threading import Thread
import logging
import asyncio
from message_processor import processMsg, start_scheduler, get_wcf_instance

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取Wcf实例，用于与微信通信
wcf = get_wcf_instance()
logging.info(f"是否已登录: {wcf.is_login()}")
logging.info(f"登录信息: {wcf.get_user_info()}")

def enableReceivingMsg():
    """
    启用消息接收功能并启动一个新线程来处理接收到的消息。
    """
    def innerWcFerryProcessMsg():
        """
        内部函数，用于在独立线程中循环处理接收到的消息。
        """
        start_scheduler()  # 启动定时任务调度器

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
