# Blue Local 部署工具使用说明

## 📦 三个部署脚本

### 1. `quick-deploy.ps1` - 一键部署（推荐）
**最简单！适合日常更新**

```powershell
# 首次使用或更新都可以
.\scripts\deployment\quick-deploy.ps1 -Server root@123.45.67.89
```

自动完成：
- ✅ 构建前端
- ✅ 提交代码到 Git
- ✅ 推送到 GitHub
- ✅ 服务器拉取更新
- ✅ 重启后端服务

---

### 2. `deploy-to-server.ps1` - 完整部署
**功能最全，适合重要更新**

```powershell
.\scripts\deployment\deploy-to-server.ps1 `
    -ServerIP "123.45.67.89" `
    -ServerUser "root" `
    -CommitMessage "添加新功能：用户管理"
```

参数说明：
- `ServerIP`: 服务器 IP 地址（必填）
- `ServerUser`: SSH 用户名（默认：root）
- `ProjectPath`: 服务器项目路径（默认：/var/www/blue-local）
- `CommitMessage`: Git 提交信息（默认：Update from local development）

---

### 3. `update-server.sh` - 服务器端更新
**在服务器上直接运行**

```bash
# SSH 登录服务器后执行
cd /var/www/blue-local
bash scripts/deployment/update-server.sh
```

仅用于服务器手动更新。

---

## 🚀 推荐工作流

### 日常开发更新（最简单）

1. **本地开发和测试**
   ```powershell
   # 启动本地后端
   python -m uvicorn backend.main:app --reload
   
   # 启动前端开发服务器
   cd frontend
   npm run dev
   ```

2. **准备部署**
   - 确保代码在本地测试通过
   - 确认所有改动已保存

3. **一键部署**
   ```powershell
   .\scripts\deployment\quick-deploy.ps1 -Server root@your-server-ip
   ```

4. **验证**
   - 访问 `http://your-server-ip` 查看效果

---

## ⚙️ 首次部署完整流程

### 步骤 1：准备服务器
- 一台 Linux 云服务器（Ubuntu/CentOS）
- 开放端口：80（HTTP）、443（HTTPS）、22（SSH）

### 步骤 2：配置 SSH 免密登录（可选但推荐）

**在本地 Windows PowerShell 执行：**
```powershell
# 生成 SSH 密钥（如果还没有）
ssh-keygen -t rsa -b 4096

# 复制公钥到服务器
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh root@your-server-ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 步骤 3：首次部署
```powershell
.\scripts\deployment\quick-deploy.ps1 -Server root@your-server-ip
```

脚本会自动：
1. 检测到是首次部署
2. 在服务器安装 Docker
3. 克隆代码
4. 创建 .env 配置文件
5. 启动所有服务

### 步骤 4：配置服务器 .env

**SSH 登录服务器：**
```bash
ssh root@your-server-ip
cd /var/www/blue-local
nano .env
```

**必须修改的配置：**
```bash
# 数据库密码（设置强密码）
DB_PASSWORD=your-strong-password

# JWT 密钥（生成随机32位字符串）
SECRET_KEY=your-random-32-character-secret-key

# 如果有域名，修改 CORS
CORS_ORIGINS=https://yourdomain.com
```

**生成随机密钥：**
```bash
openssl rand -base64 32
```

### 步骤 5：重启服务
```bash
docker-compose restart
```

### 步骤 6：验证部署
```bash
# 查看运行状态
docker-compose ps

# 查看后端日志
docker-compose logs -f backend

# 测试 API
curl http://localhost/api/health
```

---

## 📝 日常使用示例

### 场景 1：修复了一个 Bug
```powershell
# 本地测试通过后
.\scripts\deployment\quick-deploy.ps1 -Server root@123.45.67.89
```

### 场景 2：添加了新功能
```powershell
# 使用自定义提交信息
.\scripts\deployment\deploy-to-server.ps1 `
    -ServerIP "123.45.67.89" `
    -CommitMessage "feat: 添加用户权限管理功能"
```

### 场景 3：只更新后端代码
```powershell
# 1. 提交代码
git add backend/
git commit -m "update backend"
git push

# 2. SSH 到服务器
ssh root@your-server-ip

# 3. 更新
cd /var/www/blue-local
git pull
docker-compose restart backend
```

### 场景 4：只更新前端
```powershell
# 1. 构建前端
cd frontend
npm run build

# 2. 上传到服务器（Nginx 会自动使用新文件）
scp -r dist/* root@your-server-ip:/var/www/blue-local/frontend/dist/
```

---

## 🔧 故障排查

### 问题 1：部署脚本执行失败
```powershell
# 检查 PowerShell 执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新运行脚本
.\scripts\deployment\quick-deploy.ps1 -Server root@your-ip
```

### 问题 2：SSH 连接失败
```powershell
# 测试 SSH 连接
ssh root@your-server-ip

# 如果连接失败，检查：
# 1. 服务器 IP 是否正确
# 2. 防火墙是否开放 22 端口
# 3. SSH 服务是否运行
```

### 问题 3：服务器更新后无效果
```bash
# SSH 到服务器
ssh root@your-server-ip

# 强制重新构建并重启
cd /var/www/blue-local
docker-compose down
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

### 问题 4：前端更新后看不到变化
- 可能是浏览器缓存，按 `Ctrl + F5` 强制刷新
- 或者清除浏览器缓存

---

## 💡 高级技巧

### 技巧 1：设置 PowerShell 别名
在 PowerShell 配置文件中添加：
```powershell
# 编辑配置文件
notepad $PROFILE

# 添加别名
function Deploy-Blue { 
    & "d:\Laragon\laragon\www\blue-local\scripts\deployment\quick-deploy.ps1" @args 
}
Set-Alias deploy Deploy-Blue

# 以后只需输入
deploy -Server root@123.45.67.89
```

### 技巧 2：创建服务器配置文件
创建 `scripts/deployment/servers.json`：
```json
{
  "dev": {
    "ip": "123.45.67.89",
    "user": "root"
  },
  "prod": {
    "ip": "234.56.78.90",
    "user": "deploy"
  }
}
```

### 技巧 3：自动化测试后部署
```powershell
# 运行测试
python -m pytest tests/

# 测试通过后自动部署
if ($LASTEXITCODE -eq 0) {
    .\scripts\deployment\quick-deploy.ps1 -Server root@your-ip
}
```

---

## 📚 相关文档

- [环境适配完全指南](./环境适配完全指南.md)
- [Docker 部署指南](./docker部署指南.md)
- [Nginx 配置说明](../../nginx/README.md)

---

## 🆘 需要帮助？

如果遇到问题，请检查：
1. 日志文件：`docker-compose logs -f backend`
2. 服务状态：`docker-compose ps`
3. .env 配置：`cat /var/www/blue-local/.env`

或联系开发团队获取支持。
