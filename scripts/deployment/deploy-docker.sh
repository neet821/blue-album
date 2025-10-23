#!/bin/bash

# Blue Local Docker部署脚本

set -e

echo "=========================================="
echo "Blue Local Docker 一键部署"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查Docker和Docker Compose
echo -e "${GREEN}检查依赖...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker未安装${NC}"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose未安装${NC}"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker已安装${NC}"
echo -e "${GREEN}✓ Docker Compose已安装${NC}"

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}未找到.env文件，创建默认配置...${NC}"
    cp .env.docker.example .env
    
    # 生成随机密码
    MYSQL_ROOT_PASS=$(openssl rand -base64 32)
    MYSQL_USER_PASS=$(openssl rand -base64 32)
    SECRET_KEY=$(openssl rand -hex 32)
    
    # 更新.env文件
    sed -i "s/your_root_password_here/$MYSQL_ROOT_PASS/" .env
    sed -i "s/your_user_password_here/$MYSQL_USER_PASS/" .env
    sed -i "s/your_secret_key_here_use_openssl_rand_hex_32/$SECRET_KEY/" .env
    
    echo -e "${GREEN}✓ 配置文件已创建${NC}"
    echo -e "${YELLOW}密码已保存在 .env 文件中${NC}"
fi

# 构建前端
echo -e "${GREEN}构建前端...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi
npm run build
cd ..
echo -e "${GREEN}✓ 前端构建完成${NC}"

# 停止旧容器
echo -e "${GREEN}停止旧容器...${NC}"
docker-compose down

# 构建并启动容器
echo -e "${GREEN}构建并启动Docker容器...${NC}"
docker-compose up -d --build

# 等待服务启动
echo -e "${GREEN}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${GREEN}检查服务状态...${NC}"
docker-compose ps

# 显示日志
echo ""
echo "=========================================="
echo -e "${GREEN}部署完成！${NC}"
echo "=========================================="
echo ""
echo -e "${YELLOW}访问地址:${NC}"
echo "  前端: http://localhost"
echo "  API文档: http://localhost/api/docs"
echo ""
echo -e "${YELLOW}查看日志:${NC}"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f mysql"
echo "  docker-compose logs -f nginx"
echo ""
echo -e "${YELLOW}管理命令:${NC}"
echo "  启动: docker-compose start"
echo "  停止: docker-compose stop"
echo "  重启: docker-compose restart"
echo "  查看状态: docker-compose ps"
echo ""
echo -e "${RED}配置信息保存在 .env 文件中，请妥善保管！${NC}"
