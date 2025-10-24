#!/bin/bash
# ========================================
# Blue Album 服务器完整部署脚本
# 用途：首次部署或重新部署
# ========================================

set -e  # 遇到错误立即退出

PROJECT_PATH="/home/wwwroot/blue-album.top"
VENV_PATH="$PROJECT_PATH/venv"
LOG_DIR="/home/wwwlogs"

echo "========================================"
echo "  Blue Album 服务器部署脚本"
echo "========================================"
echo ""

# 1. 检查必需的软件
echo "[1/10] 检查系统环境..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 未安装"; exit 1; }
command -v nginx >/dev/null 2>&1 || { echo "❌ Nginx 未安装"; exit 1; }
command -v mysql >/dev/null 2>&1 || { echo "❌ MySQL 未安装"; exit 1; }
echo "✅ 系统环境检查通过"
echo ""

# 2. 备份旧文件
echo "[2/10] 备份旧文件..."
if [ -d "$PROJECT_PATH" ]; then
    BACKUP_NAME="blue-album.top.backup.$(date +%Y%m%d_%H%M%S)"
    mv "$PROJECT_PATH" "/home/wwwroot/$BACKUP_NAME"
    echo "✅ 旧文件已备份到 /home/wwwroot/$BACKUP_NAME"
fi
echo ""

# 3. 克隆代码
echo "[3/10] 克隆代码..."
mkdir -p /home/wwwroot
cd /home/wwwroot
git clone https://github.com/neet821/blue-album.git blue-album.top
cd blue-album.top
echo "✅ 代码克隆完成"
echo ""

# 4. 创建虚拟环境
echo "[4/10] 创建 Python 虚拟环境..."
python3 -m venv venv
source venv/bin/activate
echo "✅ 虚拟环境创建完成"
echo ""

# 5. 安装依赖
echo "[5/10] 安装 Python 依赖..."
pip install --upgrade pip
pip install -r backend/requirements.txt
echo "✅ 依赖安装完成"
echo ""

# 6. 配置 .env
echo "[6/10] 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    
    # 生成随机密钥
    SECRET_KEY=$(openssl rand -base64 32)
    
    # 替换配置
    sed -i "s/DB_NAME=blue_local_db/DB_NAME=bluealbum/" .env
    sed -i "s/DB_HOST=localhost/DB_HOST=127.0.0.1/" .env
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    sed -i "s/CORS_ORIGINS=.*/CORS_ORIGINS=https:\/\/blue-album.top,https:\/\/www.blue-album.top/" .env
    sed -i "s/ENVIRONMENT=.*/ENVIRONMENT=production/" .env
    
    echo "⚠️  请手动编辑 .env 文件，设置数据库密码："
    echo "   nano $PROJECT_PATH/.env"
    echo "   修改 DB_PASSWORD=你的密码"
    echo ""
    echo "按回车继续（编辑完成后）..."
    read
fi
echo "✅ 环境变量配置完成"
echo ""

# 7. 检查前端文件
echo "[7/10] 检查前端构建文件..."
if [ ! -d "frontend/dist" ] || [ -z "$(ls -A frontend/dist)" ]; then
    echo "⚠️  前端 dist 目录不存在或为空"
    echo "   请在本地执行 'npm run build'"
    echo "   然后上传 dist 目录到服务器："
    echo "   scp -r frontend/dist root@blue-album.top:$PROJECT_PATH/frontend/"
    echo ""
    echo "按回车继续（上传完成后）..."
    read
fi
echo "✅ 前端文件检查完成"
echo ""

# 8. 配置 Supervisor
echo "[8/10] 配置 Supervisor..."
if ! command -v supervisorctl >/dev/null 2>&1; then
    apt install supervisor -y 2>/dev/null || yum install supervisor -y
fi

cat > /etc/supervisor/conf.d/blue-album-backend.conf << EOF
[program:blue-album-backend]
command=$VENV_PATH/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
directory=$PROJECT_PATH
user=www
autostart=true
autorestart=true
stdout_logfile=$LOG_DIR/blue-album-backend.log
stderr_logfile=$LOG_DIR/blue-album-backend-error.log
environment=PYTHONPATH="$PROJECT_PATH"
EOF

mkdir -p $LOG_DIR
supervisorctl reread
supervisorctl update
supervisorctl restart blue-album-backend
echo "✅ Supervisor 配置完成"
echo ""

# 9. 配置 Nginx
echo "[9/10] 配置 Nginx..."
NGINX_CONF="/usr/local/nginx/conf/vhost/blue-album.top.conf"
if [ -f "$NGINX_CONF" ]; then
    cp "$NGINX_CONF" "$NGINX_CONF.backup.$(date +%Y%m%d_%H%M%S)"
fi

cat > "$NGINX_CONF" << 'NGINXEOF'
server {
    listen 80;
    listen [::]:80;
    server_name blue-album.top www.blue-album.top;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name blue-album.top www.blue-album.top;
    
    root /home/wwwroot/blue-album.top/frontend/dist;
    index index.html;
    
    ssl_certificate /usr/local/nginx/conf/ssl/blue-album.top/fullchain.cer;
    ssl_certificate_key /usr/local/nginx/conf/ssl/blue-album.top/blue-album.top.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 20M;
    
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(jpg|jpeg|png|gif|js|css|woff|woff2)$ {
        expires 30d;
    }
}
NGINXEOF

nginx -t && nginx -s reload
echo "✅ Nginx 配置完成"
echo ""

# 10. 设置权限
echo "[10/10] 设置文件权限..."
chown -R www:www $PROJECT_PATH
chmod -R 755 $PROJECT_PATH
echo "✅ 权限设置完成"
echo ""

# 完成
echo "========================================"
echo "🎉 部署完成！"
echo "========================================"
echo ""
echo "📋 检查清单："
echo "  1. ✅ 代码已克隆"
echo "  2. ✅ Python 依赖已安装"
echo "  3. ⚠️  请检查 .env 配置（数据库密码）"
echo "  4. ⚠️  请确保前端 dist 文件已上传"
echo "  5. ✅ Supervisor 已配置"
echo "  6. ✅ Nginx 已配置"
echo ""
echo "🔍 验证命令："
echo "  supervisorctl status"
echo "  curl http://127.0.0.1:8000/api/health"
echo "  curl -I https://blue-album.top"
echo ""
echo "📝 日志位置："
echo "  后端日志: $LOG_DIR/blue-album-backend.log"
echo "  Nginx日志: $LOG_DIR/blue-album.top.log"
echo ""
