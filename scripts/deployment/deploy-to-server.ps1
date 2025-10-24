# ========================================
# 部署脚本：本地 → 服务器
# 用途：一键推送代码并更新服务器
# ========================================

param(
    [string]$ServerIP = "",  # 服务器 IP
    [string]$ServerUser = "root",  # SSH 用户名
    [string]$ProjectPath = "/var/www/blue-local",  # 服务器项目路径
    [string]$CommitMessage = "Update from local development"  # 提交信息
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   部署到服务器" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查参数
if (-not $ServerIP) {
    $ServerIP = Read-Host "请输入服务器 IP 地址"
}

# 1. 本地构建前端
Write-Host "[1/5] 构建前端..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\..\frontend"
if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist
}
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 前端构建失败！" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 前端构建完成" -ForegroundColor Green
Write-Host ""

# 2. Git 提交
Write-Host "[2/5] 提交代码到 Git..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\.."
git add .
git commit -m "$CommitMessage" -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 代码已提交" -ForegroundColor Green
} else {
    Write-Host "⚠️  没有新的改动需要提交" -ForegroundColor Yellow
}
Write-Host ""

# 3. 推送到 GitHub
Write-Host "[3/5] 推送到 GitHub..." -ForegroundColor Yellow
git push origin master
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 推送失败！请检查网络或权限" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 代码已推送" -ForegroundColor Green
Write-Host ""

# 4. SSH 到服务器执行更新
Write-Host "[4/5] 连接服务器并更新..." -ForegroundColor Yellow
$UpdateScript = @"
cd $ProjectPath
echo '拉取最新代码...'
git pull origin master
echo '重启后端服务...'
docker-compose restart backend
echo '✅ 更新完成！'
docker-compose ps
"@

ssh ${ServerUser}@${ServerIP} $UpdateScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 服务器更新失败！" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 服务器更新完成" -ForegroundColor Green
Write-Host ""

# 5. 完成
Write-Host "[5/5] 部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🎉 部署成功！" -ForegroundColor Green
Write-Host "访问地址: http://${ServerIP}" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
