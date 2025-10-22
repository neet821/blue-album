"""
测试Socket.IO配置
"""
import urllib.request
import urllib.error

print("=" * 60)
print("Socket.IO 端点测试")
print("=" * 60)

# 测试不同的路径
test_urls = [
    "http://127.0.0.1:8000/socket.io/?EIO=4&transport=polling",
    "http://127.0.0.1:8000/ws/socket.io/?EIO=4&transport=polling",
    "http://127.0.0.1:8000/ws/?EIO=4&transport=polling",
]

for url in test_urls:
    try:
        response = urllib.request.urlopen(url, timeout=2)
        content = response.read().decode('utf-8')
        print(f"\n✅ {url}")
        print(f"   状态码: {response.status}")
        print(f"   内容: {content[:100]}")
    except urllib.error.HTTPError as e:
        print(f"\n❌ {url}")
        print(f"   HTTP错误: {e.code} - {e.reason}")
    except Exception as e:
        print(f"\n❌ {url}")
        print(f"   错误: {str(e)[:100]}")

print("\n" + "=" * 60)
