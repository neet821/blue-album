# ========================================
# 快速部署脚本（简化版）
# 用途：一键部署，自动检测是否首次部署
# ========================================

param(
    [string]$Server = ""  # 格式：user@ip，例如：root@123.45.67.89
)

$ErrorActionPreference = "Stop"

# 配置
$ProjectPath = "/var/www/blue-local"
$LocalPath = Split-Path -Parent $PSScriptRoot | Split-Path -Parent

Write-Host ""
Write-Host "🚀 Blue Local 一键部署" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查参数
if (-not $Server) {
    Write-Host "用法: .\quick-deploy.ps1 -Server user@server-ip" -ForegroundColor Yellow
    Write-Host "示例: .\quick-deploy.ps1 -Server root@123.45.67.89" -ForegroundColor Yellow
    Write-Host ""
    $Server = Read-Host "请输入服务器地址 (格式: user@ip)"
}

# 1. 构建前端
Write-Host "📦 [1/4] 构建前端..." -ForegroundColor Yellow
Push-Location "$LocalPath\frontend"
try {
    if (Test-Path "dist") { Remove-Item -Recurse -Force dist }
    npm run build | Out-Null
    Write-Host "   ✅ 前端构建完成" -ForegroundColor Green
} catch {
    Write-Host "   ❌ 前端构建失败: $_" -ForegroundColor Red
    Pop-Location
    exit 1
} finally {
    Pop-Location
}

# 2. 提交到 Git
Write-Host "📝 [2/4] 提交代码..." -ForegroundColor Yellow
Push-Location $LocalPath
try {
    git add . 2>$null
    $commitMsg = "Deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $commitMsg -q 2>$null
    git push origin master 2>&1 | Out-Null
    Write-Host "   ✅ 代码已推送到 GitHub" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  推送失败或无新改动" -ForegroundColor Yellow
} finally {
    Pop-Location
}

# 3. 检查服务器是否首次部署
Write-Host "🔍 [3/4] 检查服务器状态..." -ForegroundColor Yellow
$checkCmd = "test -d $ProjectPath && echo 'EXISTS' || echo 'NOT_EXISTS'"
$serverStatus = ssh $Server $checkCmd 2>$null

if ($serverStatus -match "NOT_EXISTS") {
    Write-Host "   ⚠️  首次部署，正在初始化服务器..." -ForegroundColor Yellow
    
    # 首次部署：克隆代码、安装 Docker、启动服务
    $initScript = @"
# 安装 Docker（如果未安装）
if ! command -v docker &> /dev/null; then
    echo '安装 Docker...'
    curl -fsSL https://get.docker.com | bash
    systemctl start docker
    systemctl enable docker
fi

# 克隆代码
echo '克隆代码...'
cd /var/www
git clone https://github.com/WTU-intelligent-software-development/development_4_10.git blue-local
cd blue-local

# 配置环境变量
cp .env.example .env
echo '请稍后手动配置 .env 文件！'

# 启动服务
echo '启动服务...'
docker-compose up -d

echo ''
echo '✅ 首次部署完成！'
echo '⚠️  请记得配置 /var/www/blue-local/.env 文件'
echo '   然后运行: docker-compose restart'
"@
    
    ssh $Server "bash -s" <<< $initScript
    
} else {
    Write-Host "   ℹ️  服务器已部署，执行更新..." -ForegroundColor Cyan
    
    # 更新部署
    $updateScript = @"
cd $ProjectPath
git pull origin master
docker-compose restart backend
echo ''
echo '✅ 更新完成！'
docker-compose ps
"@
    
    ssh $Server $updateScript
}

# 4. 完成
Write-Host "🎉 [4/4] 部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "访问地址: http://$(($Server -split '@')[1])" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
