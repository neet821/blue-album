"""测试最小化Socket.IO服务器"""
import urllib.request
import urllib.error

url = "http://127.0.0.1:8003/ws/socket.io/?EIO=4&transport=polling"
print(f"测试URL: {url}")

try:
    response = urllib.request.urlopen(url, timeout=5)
    content = response.read().decode('utf-8')
    print(f"✅ 成功! 状态码: {response.status}")
    print(f"响应内容: {content[:200]}")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP错误: {e.code} - {e.reason}")
except Exception as e:
    print(f"❌ 错误: {e}")
