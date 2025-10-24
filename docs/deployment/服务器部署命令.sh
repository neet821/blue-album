# Blue Album 服务器部署手册
# 请按步骤手动执行每个命令

## ============================================
## 第一步：备份旧文件并创建项目目录
## ============================================

# 1.1 备份旧的 blue-album.top 目录
cd /home/wwwroot/
BACKUP_NAME="blue-album.top.backup.$(date +%Y%m%d_%H%M%S)"
mv blue-album.top "$BACKUP_NAME"
echo "✅ 已备份到 $BACKUP_NAME"

# 1.2 创建新的项目目录
mkdir -p blue-album.top
cd blue-album.top
pwd  # 确认当前在 /home/wwwroot/blue-album.top


## ============================================
## 第二步：克隆代码
## ============================================

# 2.1 从 GitHub 克隆代码
git clone https://github.com/neet821/blue-album.git .

# 2.2 查看克隆的文件
ls -la

# 2.3 确认目录结构
ls backend/
ls frontend/


## ============================================
## 第三步：创建 Python 虚拟环境
## ============================================

# 3.1 创建虚拟环境
python3 -m venv venv

# 3.2 激活虚拟环境
source venv/bin/activate

# 3.3 升级 pip
pip install --upgrade pip

# 3.4 安装项目依赖
pip install -r backend/requirements.txt

# 3.5 验证安装（应该看到 fastapi, uvicorn 等）
pip list | grep -E "fastapi|uvicorn|sqlalchemy"


## ============================================
## 第四步：配置环境变量 (.env)
## ============================================

# 4.1 复制示例配置
cp .env.example .env

# 4.2 生成随机密钥（复制输出的结果）
openssl rand -base64 32

# 4.3 编辑 .env 文件
nano .env

# 请修改以下配置项：
# -----------------------------------
# DB_HOST=127.0.0.1
# DB_PASSWORD=你的MySQL密码
# DB_NAME=bluealbum
# SECRET_KEY=上面生成的随机密钥
# CORS_ORIGINS=https://blue-album.top,https://www.blue-album.top
# ENVIRONMENT=production
# HOST=127.0.0.1
# -----------------------------------
# 保存：Ctrl+O 回车
# 退出：Ctrl+X

# 4.4 验证配置（密码会隐藏）
cat .env | grep -v PASSWORD | grep -v SECRET


## ============================================
## 第五步：创建日志目录
## ============================================

# 5.1 创建日志目录
mkdir -p /home/wwwlogs

# 5.2 创建项目日志目录
mkdir -p logs

# 5.3 设置权限
chmod 755 /home/wwwlogs
chmod 755 logs


## ============================================
## 第六步：配置 Supervisor（后端进程管理）
## ============================================

# 6.1 检查 Supervisor 是否安装
supervisorctl version
# 如果未安装，执行：
# apt install supervisor -y  # Ubuntu/Debian
# 或
# yum install supervisor -y  # CentOS

# 6.2 创建 Supervisor 配置文件
cat > /etc/supervisor/conf.d/blue-album-backend.conf << 'EOF'
[program:blue-album-backend]
command=/home/wwwroot/blue-album.top/venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
directory=/home/wwwroot/blue-album.top
user=www
autostart=true
autorestart=true
stdout_logfile=/home/wwwlogs/blue-album-backend.log
stderr_logfile=/home/wwwlogs/blue-album-backend-error.log
environment=PYTHONPATH="/home/wwwroot/blue-album.top"
EOF

# 6.3 重新加载 Supervisor 配置
supervisorctl reread

# 6.4 更新 Supervisor
supervisorctl update

# 6.5 启动后端服务
supervisorctl start blue-album-backend

# 6.6 检查状态（应该显示 RUNNING）
supervisorctl status


## ============================================
## 第七步：上传并解压前端文件
## ============================================

# 7.1 确认前端目录存在
cd /home/wwwroot/blue-album.top/frontend
pwd

# 7.2 检查上传的 zip 文件
ls -lh /root/frontend-dist.zip

# 7.3 解压前端文件
unzip /root/frontend-dist.zip -d dist

# 7.4 验证前端文件
ls -la dist/
ls -la dist/assets/

# 7.5 检查 index.html
cat dist/index.html | head -10


## ============================================
## 第八步：配置 Nginx
## ============================================

# 8.1 备份原配置
cp /usr/local/nginx/conf/vhost/blue-album.top.conf \
   /usr/local/nginx/conf/vhost/blue-album.top.conf.backup.$(date +%Y%m%d_%H%M%S)

# 8.2 创建新的 Nginx 配置
cat > /usr/local/nginx/conf/vhost/blue-album.top.conf << 'EOF'
# HTTP - 自动跳转 HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name blue-album.top www.blue-album.top;
    return 301 https://$host$request_uri;
    access_log /home/wwwlogs/blue-album.top.log;
}

# HTTPS - 主配置
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name blue-album.top www.blue-album.top;
    
    # 前端静态文件根目录
    root /home/wwwroot/blue-album.top/frontend/dist;
    index index.html;
    
    # SSL 证书配置
    ssl_certificate /usr/local/nginx/conf/ssl/blue-album.top/fullchain.cer;
    ssl_certificate_key /usr/local/nginx/conf/ssl/blue-album.top/blue-album.top.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_session_cache builtin:1000 shared:SSL:10m;
    
    client_max_body_size 20M;
    
    # API 请求代理到后端
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # WebSocket 支持
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400s;
    }
    
    # 前端路由支持（Vue Router）
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location ~* \.(js|css|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 安全配置
    location ~ /\. {
        deny all;
    }
    
    access_log /home/wwwlogs/blue-album.top.log;
    error_log /home/wwwlogs/blue-album.top-error.log;
}
EOF

# 8.3 测试 Nginx 配置
nginx -t

# 8.4 如果测试通过，重新加载 Nginx
nginx -s reload

# 8.5 检查 Nginx 状态
ps aux | grep nginx | grep -v grep


## ============================================
## 第九步：设置文件权限
## ============================================

# 9.1 设置项目目录所有者为 www
cd /home/wwwroot/blue-album.top
chown -R www:www .

# 9.2 设置合适的权限
chmod -R 755 .

# 9.3 特别设置日志目录权限
chown -R www:www logs
chmod -R 755 logs

# 9.4 验证权限
ls -la /home/wwwroot/blue-album.top/ | head -15


## ============================================
## 第十步：验证部署
## ============================================

# 10.1 检查后端进程
supervisorctl status blue-album-backend

# 10.2 检查端口监听
netstat -tulpn | grep 8000

# 10.3 测试后端 API
curl http://127.0.0.1:8000/api/health
# 如果没有 /api/health 路由，测试其他接口
curl http://127.0.0.1:8000/docs

# 10.4 测试 HTTPS 访问
curl -I https://blue-album.top

# 10.5 查看后端日志（最后 20 行）
tail -20 /home/wwwlogs/blue-album-backend.log

# 10.6 如果有错误，查看错误日志
tail -20 /home/wwwlogs/blue-album-backend-error.log


## ============================================
## 常用管理命令
## ============================================

# 查看后端状态
supervisorctl status blue-album-backend

# 重启后端
supervisorctl restart blue-album-backend

# 停止后端
supervisorctl stop blue-album-backend

# 启动后端
supervisorctl start blue-album-backend

# 查看后端实时日志
tail -f /home/wwwlogs/blue-album-backend.log

# 查看 Nginx 访问日志
tail -f /home/wwwlogs/blue-album.top.log

# 查看 Nginx 错误日志
tail -f /home/wwwlogs/blue-album.top-error.log

# 重新加载 Nginx 配置
nginx -s reload

# 测试后端连接
curl http://127.0.0.1:8000/api/health


## ============================================
## 故障排查
## ============================================

# 如果后端无法启动：
# 1. 查看错误日志
tail -50 /home/wwwlogs/blue-album-backend-error.log

# 2. 手动启动测试
cd /home/wwwroot/blue-album.top
source venv/bin/activate
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
# 按 Ctrl+C 停止，然后用 Supervisor 重新启动

# 3. 检查数据库连接
mysql -u root -p -e "USE bluealbum; SHOW TABLES;"

# 4. 检查 .env 配置
cat .env | grep -E "DB_|SECRET_KEY"


## ============================================
## 部署完成检查清单
## ============================================

# ✅ 代码已克隆到 /home/wwwroot/blue-album.top
# ✅ Python 虚拟环境已创建并安装依赖
# ✅ .env 配置文件已创建并配置正确
# ✅ 前端 dist 文件已上传并解压
# ✅ Supervisor 已配置并启动后端服务
# ✅ Nginx 已配置并重新加载
# ✅ 文件权限已设置为 www:www
# ✅ 后端在 127.0.0.1:8000 正常运行
# ✅ 网站 https://blue-album.top 可以访问

## ============================================
## 完成！
## ============================================
