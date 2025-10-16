import requests
import json

url = "http://localhost:8000/api/users/register"
data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456"
}

try:
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    if response.status_code == 200:
        print("✅ 注册成功!")
    else:
        print("❌ 注册失败!")
except Exception as e:
    print(f"错误: {e}")
