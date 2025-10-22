import requests

print("测试后端 API 和 CORS 配置\n")

# 测试 1: 根路径
print("1. 测试根路径...")
try:
    response = requests.get('http://localhost:8000/')
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print(f"   ✓ 后端运行正常\n")
except Exception as e:
    print(f"   ✗ 错误: {e}\n")
    exit(1)

# 测试 2: CORS 预检请求
print("2. 测试 CORS 预检请求...")
try:
    headers = {
        'Origin': 'http://localhost:5174',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    }
    response = requests.options('http://localhost:8000/api/users/register', headers=headers)
    print(f"   状态码: {response.status_code}")
    print(f"   CORS 头: {response.headers.get('Access-Control-Allow-Origin', '未设置')}")
    
    if response.status_code == 200:
        print(f"   ✓ CORS 配置正确\n")
    else:
        print(f"   ✗ CORS 可能有问题\n")
except Exception as e:
    print(f"   ✗ 错误: {e}\n")

# 测试 3: 注册 API
print("3. 测试注册 API...")
try:
    test_data = {
        "username": f"testuser_abc123",
        "email": f"test_abc123@example.com",
        "password": "password123"
    }
    
    headers = {
        'Origin': 'http://localhost:5174',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'http://localhost:8000/api/users/register',
        json=test_data,
        headers=headers
    )
    
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
        print(f"   ✓ 注册 API 正常工作!\n")
    else:
        print(f"   响应: {response.text}")
        print(f"   ✗ 注册失败\n")
        
except Exception as e:
    print(f"   ✗ 错误: {e}\n")
    import traceback
    traceback.print_exc()

print("测试完成!")
