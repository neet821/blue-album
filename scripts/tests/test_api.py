import requests
import json

print("="*50)
print("测试后端 API")
print("="*50)

# 测试后端连接
print("\n1. 测试后端连接...")
try:
    response = requests.get('http://localhost:8000/')
    print(f"✓ 后端响应: {response.json()}")
    print(f"  状态码: {response.status_code}")
except Exception as e:
    print(f"✗ 连接失败: {e}")
    exit(1)

# 测试注册
print("\n2. 测试用户注册...")
register_data = {
    "username": "testuser999",
    "email": "test999@example.com",
    "password": "password123"
}

try:
    print(f"  发送数据: {register_data}")
    response = requests.post(
        'http://localhost:8000/api/users/register',
        json=register_data,
        timeout=10
    )
    
    print(f"  状态码: {response.status_code}")
    print(f"  响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"✓ 注册成功!")
        print(f"  返回数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"✗ 注册失败")
        print(f"  响应文本: {response.text}")
        try:
            print(f"  响应JSON: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            pass
        
except requests.exceptions.Timeout:
    print(f"✗ 请求超时")
except requests.exceptions.ConnectionError as e:
    print(f"✗ 连接错误: {e}")
except Exception as e:
    print(f"✗ 请求异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)

