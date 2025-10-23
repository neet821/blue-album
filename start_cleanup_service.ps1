# 启动后台清理任务
# 默认配置: 每5分钟检查一次，清理10分钟无人的房间

Write-Host "=" * 60
Write-Host "启动同步观影空房间清理服务" -ForegroundColor Green
Write-Host "=" * 60

# 激活虚拟环境（如果使用）
# & "venv\Scripts\Activate.ps1"

# 启动清理任务
python backend\background_tasks.py --interval 5 --timeout 10

# 参数说明:
# --interval: 检查间隔（分钟），默认5分钟
# --timeout: 空房间超时时间（分钟），默认10分钟

# 示例: 每3分钟检查一次，清理5分钟无人的房间
# python backend\background_tasks.py --interval 3 --timeout 5
