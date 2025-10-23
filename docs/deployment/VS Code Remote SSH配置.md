# VS Code Remote SSH 配置指南

## 让Copilot直接访问服务器文件

### 步骤1: 安装Remote SSH扩展

1. 打开VS Code
2. 按 `Ctrl+Shift+X` 打开扩展市场
3. 搜索 "Remote - SSH"
4. 安装 Microsoft 官方扩展

### 步骤2: 配置SSH连接

1. 按 `F1` 打开命令面板
2. 输入 "Remote-SSH: Open SSH Configuration File"
3. 选择 `C:\Users\你的用户名\.ssh\config`
4. 添加服务器配置：

```ssh-config
Host aliyun-blue-local
    HostName your-server-ip
    User root
    Port 22
    ServerAliveInterval 60
    ServerAliveCountMax 3
    # 如果使用密钥
    IdentityFile ~/.ssh/id_rsa
```

### 步骤3: 连接到服务器

1. 按 `F1` → "Remote-SSH: Connect to Host"
2. 选择 "aliyun-blue-local"
3. 输入密码（首次连接）
4. 等待VS Code Server安装完成

### 步骤4: 打开服务器上的项目

1. 点击 "打开文件夹"
2. 选择 `/var/www/blue-local` （或你的项目路径）
3. 现在Copilot可以访问服务器上的所有文件了！

## 优势

✅ Copilot可以看到服务器上的真实配置
✅ 直接在服务器上编辑文件
✅ 使用服务器的终端
✅ 自动同步，无需手动上传
✅ 支持Git操作

## 常见问题

### Q: 连接卡住不动？
A: 检查服务器防火墙，确保22端口开放

### Q: VS Code Server安装失败？
A: 服务器需要能访问外网下载VS Code Server，或手动上传

### Q: 连接自动断开？
A: 已在config中配置了ServerAliveInterval，应该不会断开
