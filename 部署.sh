#!/bin/bash
# 部署脚本：一键拉取代码并构建前端
# 用法：bash 部署.sh

echo "[1/4] 拉取最新代码..."
git pull || { echo "git pull 失败"; exit 1; }

echo "[2/4] 进入前端目录..."
cd frontend || { echo "未找到 frontend 目录"; exit 1; }

echo "[3/4] 安装前端依赖（如有变动）..."
npm install || { echo "npm install 失败"; exit 1; }

echo "[4/4] 构建前端..."
npm run build || { echo "npm run build 失败"; exit 1; }

echo "部署完成！"
