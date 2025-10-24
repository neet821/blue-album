# ========================================
# 上传文件到服务器
# ========================================

$Server = "root@blue-album.top"

Write-Host ""
Write-Host "📤 上传文件到服务器" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. 上传前端压缩包
Write-Host "[1/2] 上传前端文件..." -ForegroundColor Yellow
scp frontend-dist.zip ${Server}:/root/
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 前端文件上传成功" -ForegroundColor Green
} else {
    Write-Host "❌ 前端文件上传失败" -ForegroundColor Red
    exit 1
}

# 2. 上传部署脚本
Write-Host "[2/2] 上传部署脚本..." -ForegroundColor Yellow
scp docs/deployment/服务器部署命令.sh ${Server}:/root/
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 部署脚本上传成功" -ForegroundColor Green
} else {
    Write-Host "❌ 部署脚本上传失败" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🎉 上传完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 已上传文件：" -ForegroundColor Cyan
Write-Host "  1. /root/frontend-dist.zip" -ForegroundColor White
Write-Host "  2. /root/服务器部署命令.sh" -ForegroundColor White
Write-Host ""
Write-Host "📝 下一步：SSH 登录服务器执行部署" -ForegroundColor Yellow
Write-Host "  ssh $Server" -ForegroundColor White
Write-Host "  cat /root/服务器部署命令.sh" -ForegroundColor White
Write-Host ""
