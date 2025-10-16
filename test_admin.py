"""测试管理员功能"""
import requests

BASE_URL = "http://localhost:8000"

# 这里使用您注册的管理员账号
admin_username = "testuser"  # 替换为您的用户名
admin_password = "123456"    # 替换为您的密码

def test_admin_functions():
    print("=== 测试管理员功能 ===\n")
    
    # 1. 登录
    print("1. 登录管理员账号...")
    login_data = {
        "username": admin_username,
        "password": admin_password
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ 登录成功! Token: {token[:20]}...")
    else:
        print(f"❌ 登录失败: {response.text}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 获取当前用户信息
    print("\n2. 获取当前用户信息...")
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ 用户信息:")
        print(f"   用户名: {user['username']}")
        print(f"   邮箱: {user['email']}")
        print(f"   角色: {user['role']}")
        print(f"   状态: {'正常' if user['is_active'] else '已禁用'}")
    else:
        print(f"❌ 获取失败: {response.text}")
    
    # 3. 获取所有用户列表(管理员功能)
    print("\n3. 获取所有用户列表...")
    response = requests.get(f"{BASE_URL}/api/admin/users", headers=headers)
    
    if response.status_code == 200:
        users = response.json()
        print(f"✅ 找到 {len(users)} 个用户:")
        for u in users:
            print(f"   - {u['username']} ({u['email']}) - {u['role']} - {'正常' if u['is_active'] else '已禁用'}")
    elif response.status_code == 403:
        print("❌ 权限不足: 您不是管理员")
    else:
        print(f"❌ 获取失败: {response.text}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    try:
        test_admin_functions()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        print("请确保后端正在运行: python -m uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ 错误: {e}")
