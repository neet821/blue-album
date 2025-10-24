#!/bin/bash

# 服务器环境检查脚本
# 在服务器上运行此脚本，生成环境报告

echo "=========================================="
echo "Blue Local 服务器环境检查报告"
echo "=========================================="
echo ""

# 输出文件
REPORT_FILE="server-config-report.txt"
> $REPORT_FILE

echo "正在收集系统信息..." | tee -a $REPORT_FILE
echo "" | tee -a $REPORT_FILE

# 1. 系统信息
echo "=== 1. 系统信息 ===" | tee -a $REPORT_FILE
echo "操作系统: $(lsb_release -d | cut -f2)" | tee -a $REPORT_FILE
echo "内核版本: $(uname -r)" | tee -a $REPORT_FILE
echo "CPU核心: $(nproc)" | tee -a $REPORT_FILE
echo "总内存: $(free -h | awk '/^Mem:/ {print $2}')" | tee -a $REPORT_FILE
echo "可用内存: $(free -h | awk '/^Mem:/ {print $7}')" | tee -a $REPORT_FILE
echo "磁盘使用: $(df -h / | awk 'NR==2 {print $5}')" | tee -a $REPORT_FILE
echo "" | tee -a $REPORT_FILE

# 2. Python版本
echo "=== 2. Python环境 ===" | tee -a $REPORT_FILE
if command -v python3 &> /dev/null; then
    echo "Python版本: $(python3 --version)" | tee -a $REPORT_FILE
    echo "Python路径: $(which python3)" | tee -a $REPORT_FILE
else
    echo "❌ Python3 未安装" | tee -a $REPORT_FILE
fi

if command -v pip3 &> /dev/null; then
    echo "Pip版本: $(pip3 --version)" | tee -a $REPORT_FILE
else
    echo "❌ Pip3 未安装" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 3. Node.js版本（如需前端构建）
echo "=== 3. Node.js环境 ===" | tee -a $REPORT_FILE
if command -v node &> /dev/null; then
    echo "Node版本: $(node --version)" | tee -a $REPORT_FILE
    echo "NPM版本: $(npm --version)" | tee -a $REPORT_FILE
else
    echo "❌ Node.js 未安装（如需前端构建，需要安装）" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 4. 数据库
echo "=== 4. MySQL数据库 ===" | tee -a $REPORT_FILE
if command -v mysql &> /dev/null; then
    echo "MySQL版本: $(mysql --version)" | tee -a $REPORT_FILE
    if systemctl is-active --quiet mysql || systemctl is-active --quiet mysqld; then
        echo "状态: ✓ 运行中" | tee -a $REPORT_FILE
    else
        echo "状态: ✗ 未运行" | tee -a $REPORT_FILE
    fi
else
    echo "❌ MySQL 未安装" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 5. Web服务器
echo "=== 5. Web服务器 ===" | tee -a $REPORT_FILE
if command -v nginx &> /dev/null; then
    echo "Nginx版本: $(nginx -v 2>&1 | cut -d'/' -f2)" | tee -a $REPORT_FILE
    if systemctl is-active --quiet nginx; then
        echo "状态: ✓ 运行中" | tee -a $REPORT_FILE
    else
        echo "状态: ✗ 未运行" | tee -a $REPORT_FILE
    fi
else
    echo "❌ Nginx 未安装" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 6. 端口占用
echo "=== 6. 端口占用情况 ===" | tee -a $REPORT_FILE
echo "端口80: $(netstat -tln | grep ':80 ' > /dev/null && echo '占用' || echo '空闲')" | tee -a $REPORT_FILE
echo "端口443: $(netstat -tln | grep ':443 ' > /dev/null && echo '占用' || echo '空闲')" | tee -a $REPORT_FILE
echo "端口8000: $(netstat -tln | grep ':8000 ' > /dev/null && echo '占用' || echo '空闲')" | tee -a $REPORT_FILE
echo "端口3306: $(netstat -tln | grep ':3306 ' > /dev/null && echo '占用' || echo '空闲')" | tee -a $REPORT_FILE
echo "" | tee -a $REPORT_FILE

# 7. 防火墙状态
echo "=== 7. 防火墙配置 ===" | tee -a $REPORT_FILE
if command -v ufw &> /dev/null; then
    echo "UFW状态:" | tee -a $REPORT_FILE
    sudo ufw status | tee -a $REPORT_FILE
elif command -v firewall-cmd &> /dev/null; then
    echo "Firewalld状态:" | tee -a $REPORT_FILE
    sudo firewall-cmd --list-all | tee -a $REPORT_FILE
else
    echo "未检测到防火墙" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 8. 已安装的Python包
echo "=== 8. 已安装的Python包 ===" | tee -a $REPORT_FILE
if command -v pip3 &> /dev/null; then
    echo "检查关键依赖:" | tee -a $REPORT_FILE
    for pkg in fastapi uvicorn sqlalchemy pymysql python-socketio; do
        if pip3 list | grep -i "^$pkg " > /dev/null; then
            version=$(pip3 list | grep -i "^$pkg " | awk '{print $2}')
            echo "✓ $pkg: $version" | tee -a $REPORT_FILE
        else
            echo "✗ $pkg: 未安装" | tee -a $REPORT_FILE
        fi
    done
else
    echo "无法检查（pip3未安装）" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 9. 项目目录检查
echo "=== 9. 项目目录检查 ===" | tee -a $REPORT_FILE
if [ -d "/var/www/blue-local" ]; then
    echo "✓ 项目目录存在: /var/www/blue-local" | tee -a $REPORT_FILE
    echo "目录结构:" | tee -a $REPORT_FILE
    ls -la /var/www/blue-local | tee -a $REPORT_FILE
else
    echo "✗ 项目目录不存在（需要创建）" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

# 10. Docker检查
echo "=== 10. Docker环境 ===" | tee -a $REPORT_FILE
if command -v docker &> /dev/null; then
    echo "Docker版本: $(docker --version)" | tee -a $REPORT_FILE
    if systemctl is-active --quiet docker; then
        echo "状态: ✓ 运行中" | tee -a $REPORT_FILE
    else
        echo "状态: ✗ 未运行" | tee -a $REPORT_FILE
    fi
    
    if command -v docker-compose &> /dev/null; then
        echo "Docker Compose: $(docker-compose --version)" | tee -a $REPORT_FILE
    else
        echo "Docker Compose: 未安装" | tee -a $REPORT_FILE
    fi
else
    echo "❌ Docker 未安装" | tee -a $REPORT_FILE
fi
echo "" | tee -a $REPORT_FILE

echo "=========================================="
echo "报告生成完成: $REPORT_FILE"
echo "=========================================="
echo ""
echo "请将此文件内容复制给我，我会根据实际配置提供部署方案"
echo "查看报告: cat $REPORT_FILE"
echo "或直接复制内容: cat $REPORT_FILE | pbcopy"
