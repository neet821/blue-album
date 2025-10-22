# 阶段2 计划 — 博客文章 CRUD

目标：实现文章的创建、读取、更新、删除（CRUD），并在前端提供对应页面和编辑器。

时间框架（建议）：1-2 周

## 一、后端 API 设计（FastAPI）
- POST /api/posts              -> 创建文章（需要登录）
  - 请求体: { title: str, content: str }
  - 返回: 新文章对象
- GET /api/posts               -> 文章列表（分页、可选作者过滤）
  - 查询: ?skip=&limit=&author_id=
- GET /api/posts/{post_id}     -> 文章详情
- PUT /api/posts/{post_id}     -> 更新文章（仅作者或管理员）
- DELETE /api/posts/{post_id}  -> 删除文章（仅作者或管理员）

数据模型草案（SQLAlchemy / Pydantic）
- models.Post (已存在)
  - id, title, content, author_id, created_at, updated_at
- schemas.PostCreate / Post / PostUpdate

权限
- 创建文章：认证用户
- 编辑/删除：作者本人或 role == 'admin'

## 二、前端页面（Vue 3 + Pinia）
- /posts                -> 文章列表（分页、搜索）
- /posts/new            -> 新建文章（富文本编辑器）
- /posts/:id            -> 文章详情
- /posts/:id/edit       -> 编辑文章（仅作者或管理员）

组件
- PostList.vue
- PostCard.vue
- PostDetail.vue
- PostEditor.vue（可用简单 textarea 先实现，后续替换为富文本）

## 三、开发步骤（细分）
1. 后端：
   - 添加 Post schema（Pydantic）和 CRUD 函数
   - 添加 API 路由并实现权限检查
   - 单元测试：创建、读取、更新、删除（happy path + 授权失败）
2. 前端：
   - 新建路由与页面样式
   - 实现 PostList 与 PostDetail
   - 实现 PostEditor（先简易版）
   - 集成 API、错误处理、加载状态
3. 测试 & 修复：
   - 手动测试前端流程
   - 修复跨域、鉴权、边界情况

## 四、交付物
- 完整的后端 CRUD API 并带有简单权限测试
- 前端文章列表/详情/创建/编辑页面
- README: 运行说明与 API 文档（简要）

## 五、开始实施（下一步）
我将从后端开始：
- 在 `backend/schemas.py` 添加 `PostCreate` 与 `PostUpdate` 模型
- 在 `backend/crud.py` 添加文章相关函数
- 在 `backend/main.py` 添加文章路由

如果确认，回复“开始”，我将立即开始实现后端接口并运行快速测试。
