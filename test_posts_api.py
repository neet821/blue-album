"""测试文章 CRUD API"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 替换为您的真实登录凭据
USERNAME = "neet821"
PASSWORD = "your_password_here"  # 请替换

def test_post_crud():
    print("=== 测试文章 CRUD API ===\n")
    
    # 1. 登录获取 token
    print("1. 登录...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": USERNAME, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ 登录成功")
    
    # 2. 创建文章
    print("\n2. 创建文章...")
    new_post = {
        "title": "测试文章标题",
        "content": "这是一篇测试文章的内容。\n\n支持多段落内容。"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/posts",
        json=new_post,
        headers=headers
    )
    
    if create_response.status_code == 201:
        post = create_response.json()
        post_id = post["id"]
        print(f"✅ 文章创建成功! ID: {post_id}")
        print(f"   标题: {post['title']}")
    else:
        print(f"❌ 创建失败: {create_response.text}")
        return
    
    # 3. 获取文章列表
    print("\n3. 获取文章列表...")
    list_response = requests.get(f"{BASE_URL}/api/posts")
    
    if list_response.status_code == 200:
        posts = list_response.json()
        print(f"✅ 找到 {len(posts)} 篇文章")
        for p in posts[:3]:  # 只显示前3篇
            print(f"   - [{p['id']}] {p['title']}")
    else:
        print(f"❌ 获取失败: {list_response.text}")
    
    # 4. 获取单篇文章详情
    print(f"\n4. 获取文章 {post_id} 详情...")
    detail_response = requests.get(f"{BASE_URL}/api/posts/{post_id}")
    
    if detail_response.status_code == 200:
        post_detail = detail_response.json()
        print(f"✅ 文章详情:")
        print(f"   标题: {post_detail['title']}")
        print(f"   作者 ID: {post_detail['author_id']}")
        print(f"   内容: {post_detail['content'][:50]}...")
    else:
        print(f"❌ 获取失败: {detail_response.text}")
    
    # 5. 更新文章
    print(f"\n5. 更新文章 {post_id}...")
    update_data = {
        "title": "更新后的标题",
        "content": "这是更新后的内容。"
    }
    
    update_response = requests.put(
        f"{BASE_URL}/api/posts/{post_id}",
        json=update_data,
        headers=headers
    )
    
    if update_response.status_code == 200:
        updated = update_response.json()
        print(f"✅ 更新成功!")
        print(f"   新标题: {updated['title']}")
    else:
        print(f"❌ 更新失败: {update_response.text}")
    
    # 6. 删除文章
    print(f"\n6. 删除文章 {post_id}...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/posts/{post_id}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print(f"✅ 删除成功!")
    else:
        print(f"❌ 删除失败: {delete_response.text}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    try:
        test_post_crud()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        print("请确保后端正在运行: python -m uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ 错误: {e}")
