import aiohttp
import asyncio

async def async_request_and_respond():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:5000/repositories') as response:
            result = await response.text()
            return result

async def main():
    print("开始发送请求...")
    task = asyncio.create_task(async_request_and_respond())
    result = await task
    print("请求结果：", result)

asyncio.run(main())