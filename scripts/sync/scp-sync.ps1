param(
  [Parameter(Mandatory=$true)][string]$User,
  [Parameter(Mandatory=$true)][string]$Host,
  [Parameter(Mandatory=$true)][string]$TargetDir,
  [string]$SourceDir = (Resolve-Path ".").Path
)

$ErrorActionPreference = 'Stop'

Write-Host "[scp] Syncing $SourceDir -> $User@$Host:$TargetDir" -ForegroundColor Cyan

# 需要安装 scp（OpenSSH 客户端）
if (-not (Get-Command scp -ErrorAction SilentlyContinue)) {
  throw "scp not found. Please install OpenSSH Client."
}

scp -r -C -o StrictHostKeyChecking=no `
  "$SourceDir/*" `
  "$User@$Host:$TargetDir/"

Write-Host "[done] Files copied via SCP." -ForegroundColor Green
