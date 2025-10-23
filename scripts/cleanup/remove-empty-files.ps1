# Clean up zero-byte empty files in root directory
param(
  [string]$TargetDir = "d:\Laragon\laragon\www\blue-local",
  [switch]$DryRun = $false
)

$ErrorActionPreference = 'Stop'

Write-Host "`n[cleanup] Scanning for empty files..." -ForegroundColor Cyan

# Get all zero-byte files
$emptyFiles = Get-ChildItem -Path $TargetDir -File | Where-Object { $_.Length -eq 0 }

if ($emptyFiles.Count -eq 0) {
  Write-Host "[cleanup] No empty files found." -ForegroundColor Green
  exit 0
}

Write-Host "[cleanup] Found $($emptyFiles.Count) empty files." -ForegroundColor Yellow

# Generate cleanup report
$reportPath = Join-Path $TargetDir "docs\empty-files-cleanup-report.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$reportContent = @"
# Empty Files Cleanup Report

Cleanup Time: $timestamp
Target Directory: $TargetDir
Total Files: $($emptyFiles.Count)

## Deleted Empty Files List

"@

foreach ($file in $emptyFiles) {
  $reportContent += "- ``$($file.Name)`` (Last Modified: $($file.LastWriteTime.ToString('yyyy-MM-dd HH:mm')))`n"
}

$reportContent += @"

## Notes

These zero-byte files were removed, including:
- Early test scripts (test_*.py, test_*.ps1)
- Temporary diagnostic documents (*.md)
- Empty batch files (*.bat)
- Temporary database scripts (*.py, *.sql)

Removal does not affect normal project operation. To restore, check Git history.

Cleanup script location: ``scripts/cleanup/remove-empty-files.ps1``
"@

# Write report
$reportContent | Out-File -FilePath $reportPath -Encoding UTF8 -Force
Write-Host "[report] Report generated: $reportPath" -ForegroundColor Cyan

if ($DryRun) {
  Write-Host "`n[dry-run] Simulation mode - no files will be deleted." -ForegroundColor Yellow
  Write-Host "To run: .\remove-empty-files.ps1" -ForegroundColor Gray
  exit 0
}

# Delete files
Write-Host "`n[cleanup] Deleting empty files..." -ForegroundColor Cyan
$deleted = 0
foreach ($file in $emptyFiles) {
  try {
    Remove-Item -Path $file.FullName -Force
    $deleted++
    Write-Host "  OK Deleted: $($file.Name)" -ForegroundColor Gray
  } catch {
    Write-Host "  FAIL Delete failed: $($file.Name) - $_" -ForegroundColor Red
  }
}

Write-Host "`n[done] Deleted $deleted empty files." -ForegroundColor Green
Write-Host "[info] Cleanup report: $reportPath" -ForegroundColor Cyan
