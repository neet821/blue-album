#!/bin/bash

# Blue Local 项目一键部署脚本
# 适用于 Ubuntu/Debian 系统

set -e  # 遇到错误立即退出

echo "=========================================="
echo "Blue Local 项目部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 配置变量
PROJECT_DIR="/var/www/blue-local"
VENV_DIR="$PROJECT_DIR/venv"
DB_NAME="blue_local_db"
DB_USER="blue_local_user"
DB_PASS=$(openssl rand -base64 32)  # 生成随机密码

echo -e "${GREEN}1. 安装系统依赖...${NC}"
apt-get update
apt-get install -y python3-pip python3-venv nginx supervisor mysql-server

echo -e "${GREEN}2. 创建Python虚拟环境...${NC}"
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo -e "${GREEN}3. 安装Python依赖...${NC}"
pip install -r $PROJECT_DIR/backend/requirements.txt

echo -e "${GREEN}4. 配置MySQL数据库...${NC}"
mysql -u root <<MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo -e "${GREEN}5. 创建环境配置文件...${NC}"
cat > $PROJECT_DIR/backend/.env <<EOF
DATABASE_URL=mysql+pymysql://$DB_USER:$DB_PASS@localhost:3306/$DB_NAME
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
ALLOWED_HOSTS=*
EOF

echo -e "${GREEN}6. 配置Supervisor（后端服务）...${NC}"
cat > /etc/supervisor/conf.d/blue-local-backend.conf <<EOF
[program:blue-local-backend]
command=$VENV_DIR/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
directory=$PROJECT_DIR
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/blue-local-backend.log
environment=PYTHONPATH="$PROJECT_DIR"
EOF

echo -e "${GREEN}7. 配置Supervisor（清理服务）...${NC}"
cat > /etc/supervisor/conf.d/blue-local-cleanup.conf <<EOF
[program:blue-local-cleanup]
command=$VENV_DIR/bin/python backend/background_tasks.py
directory=$PROJECT_DIR
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/blue-local-cleanup.log
EOF

echo -e "${GREEN}8. 配置Nginx...${NC}"
cat > /etc/nginx/sites-available/blue-local <<'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 20M;

    # 前端静态文件
    location / {
        root /var/www/blue-local/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # WebSocket代理
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        root /var/www/blue-local/frontend/dist;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/blue-local /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo -e "${GREEN}9. 设置文件权限...${NC}"
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

echo -e "${GREEN}10. 启动服务...${NC}"
supervisorctl reread
supervisorctl update
supervisorctl start blue-local-backend
supervisorctl start blue-local-cleanup

nginx -t
systemctl restart nginx

echo -e "${GREEN}=========================================="
echo "部署完成！"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}数据库信息：${NC}"
echo "  数据库名: $DB_NAME"
echo "  用户名: $DB_USER"
echo "  密码: $DB_PASS"
echo ""
echo -e "${YELLOW}服务状态检查：${NC}"
echo "  supervisorctl status"
echo ""
echo -e "${YELLOW}查看日志：${NC}"
echo "  tail -f /var/log/blue-local-backend.log"
echo "  tail -f /var/log/blue-local-cleanup.log"
echo ""
echo -e "${YELLOW}访问地址：${NC}"
echo "  http://your-server-ip"
echo ""
echo -e "${RED}⚠️  请保存好数据库密码！${NC}"
