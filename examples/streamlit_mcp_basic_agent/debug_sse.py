import asyncio
import logging
from mcp.client.sse import sse_client

# 设置详细日志
logging.basicConfig(level=logging.DEBUG)

async def test_sse_connection():
    url = "https://router.mcp.so/sse/9ojqzbm8k3nvg1"
    print(f"尝试连接到SSE服务器: {url}")
    
    try:
        async with sse_client(url) as (read_stream, write_stream):
            print("连接成功！")
            # 发送一个简单的ping消息
            print("发送ping消息...")
            await write_stream.send({"jsonrpc": "2.0", "method": "ping", "id": 1})
            
            # 等待响应
            print("等待响应...")
            response = await read_stream.receive()
            print(f"接收到响应: {response}")
            
    except Exception as e:
        print(f"连接失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sse_connection()) 