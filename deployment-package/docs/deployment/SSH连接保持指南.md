# SSH保持连接配置指南

## 问题：SSH连接自动断开

### 方案1: 客户端配置（推荐）

创建或编辑SSH配置文件：

**Windows:** `C:\Users\你的用户名\.ssh\config`

```bash
# 添加以下内容
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes

# 或针对特定服务器
Host aliyun-server
    HostName your-server-ip
    User root
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**说明：**
- `ServerAliveInterval 60`: 每60秒发送一次心跳包
- `ServerAliveCountMax 3`: 最多3次无响应后断开
- 这样可以保持连接最多180秒无响应

### 方案2: 服务器端配置

SSH连接到服务器后，编辑配置：

```bash
sudo vim /etc/ssh/sshd_config

# 添加或修改以下配置
ClientAliveInterval 60
ClientAliveCountMax 3
TCPKeepAlive yes

# 保存后重启SSH服务
sudo systemctl restart sshd
```

### 方案3: 使用screen或tmux（强烈推荐）

即使SSH断开，进程也会继续运行：

```bash
# 安装screen
sudo apt-get install screen

# 创建会话
screen -S deploy

# 在screen中工作
# 如果断开，重新连接后恢复
ssh user@server
screen -r deploy

# 或使用tmux
sudo apt-get install tmux
tmux new -s deploy
# 断开后恢复: tmux attach -t deploy
```

### 方案4: 使用MobaXterm（Windows最佳工具）

下载地址: https://mobaxterm.mobatek.net/

优点：
- 自动保持连接
- 内置SFTP文件传输
- 支持多标签
- 会话管理
- 完全免费（个人版）
