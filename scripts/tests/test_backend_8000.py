"""测试8000端口Backend"""
import http.client
import time

print("等待后端启动...")
time.sleep(2)

print("\n测试Backend 8000端口的Socket.IO端点:")
print("=" * 60)

try:
    conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=10)
    path = "/ws/socket.io/?EIO=4&transport=polling"
    
    print(f"请求: GET {path}")
    conn.request("GET", path)
    
    response = conn.getresponse()
    body = response.read()
    
    print(f"\n✅ 状态码: {response.status}")
    print(f"✅ 响应长度: {len(body)} 字节")
    print(f"✅ 响应内容前200字符:")
    print(body[:200])
    
    if response.status == 200:
        print("\n🎉 Socket.IO端点工作正常！")
    else:
        print(f"\n❌ 返回错误状态码: {response.status}")
    
    conn.close()
    
except ConnectionRefusedError:
    print("❌ 连接被拒绝 - 后端可能未启动")
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("=" * 60)
