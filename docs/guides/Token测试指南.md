# 🔍 Token 自动注入测试指南

**创建时间:** 2025年10月16日

---

## 📋 测试目标

验证 `frontend/src/utils/request.js` 拦截器是否正确自动注入 Authorization token。

---

## ✅ 正确的测试方法

### 步骤 1: 登录系统
1. 访问 http://localhost:5173/login
2. 输入用户名和密码登录
3. 确认成功跳转到首页

### 步骤 2: 打开开发者工具
1. 按 `F12` 或右键 → 检查
2. 切换到 **Network(网络)** 标签
3. 点击 🚫 图标清空日志

### 步骤 3: 访问链接管理工具
1. 点击导航栏 "工具" → "链接管理工具"
2. 或直接访问 http://localhost:5173/tools/link-dashboard

### 步骤 4: 筛选 API 请求
在 Network 标签的 Filter(筛选器)中:
- 输入 `api` 或 `/api`
- 或点击 `Fetch/XHR` 按钮只显示 AJAX 请求

### 步骤 5: 检查请求头
找到这些 API 请求(至少会有这两个):
- ✅ `http://localhost:8000/api/categories` (GET)
- ✅ `http://localhost:8000/api/links?category_id=xxx` (GET)

点击其中一个请求:
1. 切换到 **Headers(标头)** 标签
2. 向下滚动找到 **Request Headers(请求标头)**
3. 查找 `Authorization` 字段

### 步骤 6: 验证 Token
应该看到类似这样的内容:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTcyOTM0NTY3OH0.xxx
```

✅ **测试通过:** 如果看到 `Authorization: Bearer <一长串token>`

❌ **测试失败:** 如果没有 `Authorization` 字段

---

## ❌ 常见错误 - 不要检查静态资源

### 错误示例
你之前检查的是:
```
请求 URL: http://localhost:5173/vite.svg
```

这是一个**静态图片资源**,**不应该**也**不会**包含 Authorization token。

### 静态资源列表(不包含 token)
- `*.svg` - SVG 图片
- `*.png`, `*.jpg`, `*.ico` - 其他图片
- `*.js`, `*.css` - 前端资源文件
- `/assets/*` - Vite 打包的静态资源

这些资源是前端文件,不需要后端认证!

---

## 🎯 只有这些请求才需要 Token

### API 请求特征
1. URL 以 `/api` 开头
2. 实际请求地址是 `http://localhost:8000/api/...` (后端端口 8000)
3. 类型通常是 `fetch` 或 `xhr`

### 常见 API 请求示例
| 请求 | 方法 | 用途 | 需要 Token |
|------|------|------|------------|
| `/api/auth/login` | POST | 登录 | ❌ 不需要 |
| `/api/auth/register` | POST | 注册 | ❌ 不需要 |
| `/api/auth/me` | GET | 获取当前用户 | ✅ 需要 |
| `/api/categories` | GET | 获取分类列表 | ✅ 需要 |
| `/api/categories` | POST | 创建分类 | ✅ 需要 |
| `/api/links` | GET | 获取链接列表 | ✅ 需要 |
| `/api/links` | POST | 创建链接 | ✅ 需要 |
| `/vite.svg` | GET | 静态图片 | ❌ 不需要 |

---

## 🔍 更详细的检查方法

### 方法 1: 使用 Console 查看
在开发者工具的 Console 中运行:
```javascript
// 查看当前 token
localStorage.getItem('token')

// 查看 token 解码后的内容(需要 jwt-decode 库或在线工具)
```

### 方法 2: 使用 Postman/Insomnia 测试
1. 复制 localStorage 中的 token
2. 在 Postman 中创建请求:
   - URL: `http://localhost:8000/api/categories`
   - Method: `GET`
   - Headers: `Authorization: Bearer <你的token>`
3. 发送请求,应该返回 200 OK

### 方法 3: 故意发送错误 token
1. 在浏览器 Console 中运行:
   ```javascript
   localStorage.setItem('token', 'fake-token-123')
   ```
2. 刷新链接管理页面
3. 应该自动跳转到登录页(因为 401 错误)

---

## 📸 测试截图建议

完整的测试应包含这些截图:

### 截图 1: LocalStorage 中的 Token
- 开发者工具 → Application → Local Storage → http://localhost:5173
- 显示 `token` 键值对

### 截图 2: API 请求列表
- Network 标签,筛选器输入 `api`
- 显示多个 API 请求(categories, links 等)

### 截图 3: Request Headers
- 点击某个 API 请求 → Headers 标签
- 高亮显示 `Authorization: Bearer ...` 行

### 截图 4: 静态资源对比
- 展示静态资源请求(如 vite.svg)
- 证明**没有** Authorization 头部

---

## ✅ 测试检查清单

- [ ] 能在 Network 中找到 API 请求(以 /api 开头)
- [ ] API 请求的 Headers 中包含 Authorization
- [ ] Token 格式正确(Bearer + JWT)
- [ ] 静态资源请求**不包含** Authorization
- [ ] 删除 token 后刷新页面会自动跳转登录
- [ ] 使用错误 token 会触发 401 错误

---

## 🐛 如果测试失败

### 问题 1: 没有看到 API 请求
**原因:** 可能链接管理页面加载失败  
**解决:** 检查后端服务器是否运行,查看 Console 是否有错误

### 问题 2: API 请求没有 Authorization
**原因:** request.js 拦截器未生效  
**解决:** 
1. 确认使用的是 `request` 实例,不是原生 `axios`
2. 检查 LinkDashboard.vue 是否导入了 `@/utils/request`

### 问题 3: Token 格式错误
**原因:** localStorage 中的 token 可能损坏  
**解决:** 
1. 清空 localStorage: `localStorage.clear()`
2. 重新登录

---

**总结:** 只检查 `/api` 开头的请求,忽略所有静态资源!
