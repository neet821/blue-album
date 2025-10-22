# 测试同步观影 API

Write-Host "=== 测试同步观影 API ===" -ForegroundColor Green

# 测试1: 获取房间列表（无需认证）
Write-Host "`n1. 测试获取房间列表..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/sync-rooms" -Method GET
    Write-Host "✅ 成功: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ 失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 测试2: 检查 WebSocket 挂载
Write-Host "`n2. 测试 WebSocket 路径..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/ws/" -Method GET
    Write-Host "✅ WebSocket 已挂载: $($response.StatusCode)" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 426) {
        Write-Host "✅ WebSocket 正常 (426 Upgrade Required)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  状态码: $($_.Exception.Response.StatusCode)" -ForegroundColor Yellow
    }
}

# 测试3: 健康检查
Write-Host "`n3. 测试根路径..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET
    Write-Host "✅ 成功: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ 失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== 测试完成 ===" -ForegroundColor Green
