# 📚 文档和脚本目录索引

本项目的所有文档和脚本已整理到以下目录结构中：

---

## 📁 目录结构

```
blue-local/
├── docs/                    # 📖 文档目录
│   ├── architecture/        # 🏗️ 架构设计文档
│   ├── guides/              # 📘 使用指南和教程
│   ├── reports/             # 📋 问题修复报告
│   └── summaries/           # 📊 阶段总结文档
│
├── scripts/                 # 🔧 脚本目录
│   ├── database/            # 💾 数据库相关脚本
│   ├── tests/               # 🧪 测试脚本
│   └── utils/               # 🛠️ 工具脚本
│
├── backend/                 # 后端代码
├── frontend/                # 前端代码
└── README.md                # 项目说明
```

---

## 📖 文档分类

### 🏗️ 架构设计文档 (`docs/architecture/`)
项目架构分析和设计文档：
- `项目架构分析_总览.md`
- `项目架构分析_第1部分.md`
- `项目架构分析_第2部分.md`
- `项目架构分析_第3部分.md`
- `项目架构分析_第4部分.md`

### 📘 使用指南和教程 (`docs/guides/`)
功能使用说明、配置指南、测试指南：
- 功能指南
  - `同步观影_快速开始.md`
  - `链接管理工具使用指南.md`
  - `暗黑模式使用指南.md`
  - `管理员系统使用指南.md`
  
- 测试指南
  - `401测试指南.md`
  - `Token测试指南.md`
  - `测试清单.md`
  - `路由保护测试.md`
  - `请求超时测试指南.md`
  - `超时测试快速开始.md`
  
- 配置说明
  - `端口配置说明.md`
  - `立即开始.md`
  
- 教程
  - `视频URL抓取教程.md`

### 📋 问题修复报告 (`docs/reports/`)
各类问题的诊断和修复记录：
- WebSocket相关
  - `WebSocket修复完成.md`
  - `同步观影_NotFound修复完成.md`
  - `卡顿和序列化问题修复.md`
  
- 功能修复
  - `URL重复问题修复完成.md`
  - `axios迁移修复报告.md`
  - `路径别名问题修复.md`
  - `用户问题修复报告.md`
  - `管理员界面_修复完成.md`
  
- 问题诊断
  - `401问题诊断.md`
  - `bcrypt问题解决.md`
  - `解决500错误.md`
  - `故障排查指南.md`
  - `同步观影_功能诊断指南.md`
  - `同步观影_快速诊断修复.md`
  - `管理员界面_角色状态显示问题诊断.md`

### 📊 阶段总结文档 (`docs/summaries/`)
项目各阶段的开发总结：
- 阶段总结
  - `阶段1_用户与管理员系统总结.md`
  - `阶段2_博客CRUD计划.md`
  - `阶段2_完成总结.md`
  - `阶段2.5_四大功能扩展总结.md`
  - `阶段3_高级功能开发.md`
  - `阶段3.1_暗黑模式完成总结.md`
  
- 功能总结
  - `第一阶段完成总结.md`
  - `同步观影功能_实施总结.md`
  - `网站收藏管理完成总结.md`
  
- 更新说明
  - `管理员文章权限更新说明.md`
  - `显示作者名称更新说明.md`

---

## 🔧 脚本分类

### 💾 数据库脚本 (`scripts/database/`)
数据库初始化、迁移、维护脚本：
- `init_database.py` - 数据库初始化
- `create_db_tables.py` - 创建数据库表
- `create_tables.sql` - SQL建表脚本
- `update_database.py` - 数据库更新
- `check_database.py` - 检查数据库状态
- `add_category_to_posts.py` - 为文章添加分类字段
- `add_views_to_posts.py` - 为文章添加浏览次数字段
- `check_test_user.py` - 检查test用户状态
- `fix_test_user.py` - 修复test用户
- `verify_mount.py` - 验证挂载点

### 🧪 测试脚本 (`scripts/tests/`)
各类功能测试脚本：
- API测试
  - `test_api.py` - API综合测试
  - `test_posts_api.py` - 文章API测试
  - `test_admin.py` - 管理员功能测试
  - `test_register.py` - 注册功能测试
  
- 后端测试
  - `test_backend_8000.py` - 8000端口测试
  - `test_backend_full.py` - 后端完整测试
  - `test_8002.py` - 8002端口测试
  
- 连接测试
  - `test_connection.py` - 连接测试
  - `test_db_connection.py` - 数据库连接测试
  - `test_cors.py` - CORS测试
  
- Socket.IO测试
  - `test_socketio.py` - Socket.IO Python测试
  - `test_socketio.html` - Socket.IO浏览器测试
  - `test_websocket_import.py` - WebSocket导入测试
  - `test_standalone.py` - 独立服务器测试
  
- 其他测试
  - `test_endpoints.py` - 端点测试
  - `test_import.py` - 导入测试
  - `test_minimal.py` - 最小化测试
  - `test_minimal_client.py` - 最小化客户端测试
  - `test_database.py` - 数据库测试
  - `test_user_operations.py` - 用户操作测试
  - `test_sync_api.ps1` - 同步API测试（PowerShell）

### 🛠️ 工具脚本 (`scripts/utils/`)
通用工具和辅助脚本：
- `standalone_socketio.py` - 独立Socket.IO服务器
- `minimal_socketio_test.py` - 最小化Socket.IO测试
- `quick_test.py` - 快速测试工具

---

## 🚀 快速访问

### 新手入门
1. 📖 阅读 `立即开始.md` 了解项目基础
2. 📘 查看 `端口配置说明.md` 了解服务端口
3. 🔧 运行 `scripts/database/init_database.py` 初始化数据库

### 功能使用
- 同步观影: `docs/guides/同步观影_快速开始.md`
- 管理员系统: `docs/guides/管理员系统使用指南.md`
- 暗黑模式: `docs/guides/暗黑模式使用指南.md`
- 链接管理: `docs/guides/链接管理工具使用指南.md`

### 问题排查
1. 🔍 查看 `docs/reports/故障排查指南.md`
2. 🔍 查看具体功能的诊断指南
3. 🧪 运行对应的测试脚本验证问题

### 开发参考
- 架构设计: `docs/architecture/`
- 阶段总结: `docs/summaries/`
- 修复报告: `docs/reports/`

---

## 📌 注意事项

1. **批处理脚本**: 根目录保留了 `安装前端依赖.bat` 和 `安装后端依赖.bat`，方便快速安装依赖
2. **README文件**: 各功能模块的README保留在原位置
3. **配置文件**: package.json、.gitignore等配置文件保留在根目录
4. **运行脚本**: 所有Python脚本需要在项目根目录运行

---

## 🔄 更新日志

### 2025-10-22
- ✅ 整理所有文档到 `docs/` 目录
- ✅ 整理所有脚本到 `scripts/` 目录
- ✅ 创建子目录分类管理
- ✅ 创建本索引文档

---

**维护者**: 项目团队  
**最后更新**: 2025-10-22
