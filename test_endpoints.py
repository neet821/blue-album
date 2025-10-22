"""测试所有端点"""
import http.client
import json

def test_endpoint(path, description):
    print(f"\n测试: {description}")
    print(f"路径: {path}")
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 8005, timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read().decode('utf-8')
        print(f"✅ 状态码: {response.status}")
        print(f"   响应: {body[:200]}")
        conn.close()
        return response.status
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

print("=" * 60)
print("测试8005端口的所有端点")
print("=" * 60)

# 测试基础路由
test_endpoint("/", "FastAPI根路径")
test_endpoint("/health", "健康检查")

# 测试Socket.IO端点（不同的可能路径）
test_endpoint("/socket.io/", "直接Socket.IO路径")
test_endpoint("/socket.io/?EIO=4&transport=polling", "Socket.IO带参数")
test_endpoint("/ws/socket.io/", "挂载点+Socket.IO路径")
test_endpoint("/ws/socket.io/?EIO=4&transport=polling", "完整Socket.IO端点")
test_endpoint("/ws/", "仅挂载点")
test_endpoint("/ws", "挂载点无斜杠")

print("\n" + "=" * 60)
