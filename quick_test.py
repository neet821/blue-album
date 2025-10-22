"""快速测试Socket.IO端点"""
import urllib.request

urls = [
    "http://127.0.0.1:8000/ws/socket.io/?EIO=4&transport=polling",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'Connection': 'close'})
        response = urllib.request.urlopen(req, timeout=3)
        content = response.read().decode('utf-8')
        print(f"✅ {url}")
        print(f"   状态: {response.status}")
        print(f"   内容前100字符: {content[:100]}\n")
    except Exception as e:
        print(f"❌ {url}")
        print(f"   错误: {str(e)}\n")
