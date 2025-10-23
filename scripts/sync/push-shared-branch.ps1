param(
  [string]$Branch = "shared/win-sync",
  [string]$Message = "sync: update at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
)

$ErrorActionPreference = 'Stop'

Write-Host "[sync] Checking repo..." -ForegroundColor Cyan
git rev-parse --is-inside-work-tree | Out-Null

Write-Host "[sync] Fetching origin..." -ForegroundColor Cyan
git fetch origin

Write-Host "[sync] Switching to branch $Branch ..." -ForegroundColor Cyan
git checkout -B $Branch

Write-Host "[sync] Staging changes..." -ForegroundColor Cyan
git add -A

try {
  git commit -m $Message
} catch {
  Write-Host "[sync] Nothing to commit (working tree clean)." -ForegroundColor Yellow
}

Write-Host "[sync] Pushing to origin/$Branch ..." -ForegroundColor Cyan
git push -u origin $Branch

Write-Host "`n[done] Local -> origin synced. On server, run:" -ForegroundColor Green
Write-Host "  git fetch origin" -ForegroundColor Gray
Write-Host "  git checkout -B $Branch origin/$Branch" -ForegroundColor Gray
Write-Host "  git pull --ff-only" -ForegroundColor Gray
