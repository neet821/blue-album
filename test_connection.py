import http.client
import json

print("测试后端连接...")

try:
    # 测试根路径
    conn = http.client.HTTPConnection("localhost", 8000, timeout=5)
    conn.request("GET", "/")
    response = conn.getresponse()
    
    print(f"✅ 状态码: {response.status}")
    print(f"✅ 响应: {response.read().decode()}")
    
    conn.close()
    
    print("\n测试完成! 后端正常运行。")
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("\n可能原因:")
    print("1. 后端未启动")
    print("2. 端口被占用")
    print("3. 防火墙阻止")
