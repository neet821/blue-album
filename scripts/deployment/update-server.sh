#!/bin/bash
# ========================================
# 服务器更新脚本
# 用途：在服务器上执行，拉取最新代码并重启服务
# ========================================

PROJECT_PATH="/var/www/blue-local"
cd "$PROJECT_PATH" || exit 1

echo "================================"
echo "   更新服务器代码"
echo "================================"
echo ""

# 1. 拉取最新代码
echo "[1/3] 拉取最新代码..."
git pull origin master
if [ $? -ne 0 ]; then
    echo "❌ 拉取代码失败！"
    exit 1
fi
echo "✅ 代码已更新"
echo ""

# 2. 重启后端服务
echo "[2/3] 重启后端服务..."
docker-compose restart backend
if [ $? -ne 0 ]; then
    echo "❌ 重启失败！"
    exit 1
fi
echo "✅ 服务已重启"
echo ""

# 3. 显示运行状态
echo "[3/3] 检查运行状态..."
docker-compose ps
echo ""

echo "================================"
echo "🎉 更新完成！"
echo "================================"
