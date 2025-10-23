@echo off
chcp 65001 >nul
echo ==========================================
echo Blue Local 项目打包脚本
echo ==========================================
echo.

set PROJECT_DIR=%~dp0..\..
set OUTPUT_DIR=%PROJECT_DIR%\deploy-package
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo 📦 开始打包项目...
echo.

REM 创建输出目录
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%\backend"
mkdir "%OUTPUT_DIR%\frontend"
mkdir "%OUTPUT_DIR%\scripts"
mkdir "%OUTPUT_DIR%\docs"

echo ✓ 1/6 复制后端文件...
xcopy "%PROJECT_DIR%\backend\*.py" "%OUTPUT_DIR%\backend\" /Y /Q
xcopy "%PROJECT_DIR%\backend\requirements.txt" "%OUTPUT_DIR%\backend\" /Y /Q
echo     - Python源文件已复制

echo ✓ 2/6 构建前端...
cd "%PROJECT_DIR%\frontend"
call npm run build
if errorlevel 1 (
    echo ❌ 前端构建失败！
    pause
    exit /b 1
)
xcopy "%PROJECT_DIR%\frontend\dist" "%OUTPUT_DIR%\frontend\dist\" /E /I /Y /Q
echo     - 前端构建完成

echo ✓ 3/6 复制部署脚本...
xcopy "%PROJECT_DIR%\scripts\deployment\deploy.sh" "%OUTPUT_DIR%\scripts\" /Y /Q
xcopy "%PROJECT_DIR%\scripts\database\*.py" "%OUTPUT_DIR%\scripts\database\" /E /I /Y /Q
echo     - 部署脚本已复制

echo ✓ 4/6 复制文档...
xcopy "%PROJECT_DIR%\docs\deployment" "%OUTPUT_DIR%\docs\deployment\" /E /I /Y /Q
xcopy "%PROJECT_DIR%\README.md" "%OUTPUT_DIR%\" /Y /Q
echo     - 文档已复制

echo ✓ 5/6 创建环境配置模板...
(
echo DATABASE_URL=mysql+pymysql://username:password@localhost:3306/blue_local_db
echo SECRET_KEY=change-this-to-random-secret-key
echo DEBUG=False
echo ALLOWED_HOSTS=*
) > "%OUTPUT_DIR%\backend\.env.example"
echo     - 配置模板已创建

echo ✓ 6/6 创建部署说明...
(
echo # Blue Local 项目部署包
echo.
echo 生成时间: %TIMESTAMP%
echo.
echo ## 📦 包含内容
echo.
echo - backend/         后端Python代码
echo - frontend/dist/   前端构建产物
echo - scripts/         部署和数据库脚本
echo - docs/            部署文档
echo.
echo ## 🚀 快速部署（Linux服务器）
echo.
echo 1. 上传整个目录到服务器 /var/www/blue-local
echo 2. 进入目录: cd /var/www/blue-local
echo 3. 给脚本执行权限: chmod +x scripts/deploy.sh
echo 4. 运行部署: sudo ./scripts/deploy.sh
echo 5. 访问: http://your-server-ip
echo.
echo ## ⚙️  手动部署步骤
echo.
echo 详见 docs/deployment/部署检查清单.md
echo.
echo ## 🔐 环境配置
echo.
echo 1. 复制 backend/.env.example 为 backend/.env
echo 2. 修改数据库连接信息
echo 3. 生成随机SECRET_KEY
echo.
echo ## 📝 数据库初始化
echo.
echo 运行迁移脚本:
echo python scripts/database/add_member_online_status.py
echo.
echo ## 🆘 需要帮助？
echo.
echo 查看完整文档: docs/deployment/部署检查清单.md
) > "%OUTPUT_DIR%\README.txt"

echo.
echo ==========================================
echo ✅ 打包完成！
echo ==========================================
echo.
echo 📁 输出目录: %OUTPUT_DIR%
echo.
echo 📊 文件统计:
dir /s /b "%OUTPUT_DIR%\*.*" | find /c /v "" 
echo     个文件已打包
echo.
echo 💡 下一步:
echo 1. 压缩 deploy-package 目录
echo 2. 上传到服务器
echo 3. 运行 scripts/deploy.sh
echo.
pause
