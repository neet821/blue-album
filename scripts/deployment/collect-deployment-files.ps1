# Collect all deployment-related files for server deployment
param(
  [string]$OutputDir = "deployment-package",
  [switch]$IncludeFrontendBuild = $false
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = "d:\Laragon\laragon\www\blue-local"

Write-Host "`n[collect] Collecting deployment files..." -ForegroundColor Cyan
Write-Host "[info] Project root: $ProjectRoot" -ForegroundColor Gray

# Create output directory
$PackageDir = Join-Path $ProjectRoot $OutputDir
if (Test-Path $PackageDir) {
  Write-Host "[clean] Removing existing package directory..." -ForegroundColor Yellow
  Remove-Item -Path $PackageDir -Recurse -Force
}
New-Item -Path $PackageDir -ItemType Directory | Out-Null
Write-Host "[ok] Created package directory: $PackageDir" -ForegroundColor Green

# Define file lists
$FilesToCopy = @(
  # Root config files
  "Dockerfile",
  "docker-compose.yml",
  ".env.docker.example",
  "package.json",
  "start_cleanup_service.ps1",
  
  # Backend (entire directory)
  "backend",
  
  # Frontend source (for building on server)
  "frontend/src",
  "frontend/public",
  "frontend/index.html",
  "frontend/package.json",
  "frontend/vite.config.ts",
  "frontend/vite.config.js",
  "frontend/tsconfig.json",
  "frontend/tsconfig.node.json",
  
  # Nginx config
  "nginx",
  
  # Deployment scripts
  "scripts/deployment/deploy.sh",
  "scripts/deployment/deploy-docker.sh",
  "scripts/deployment/check-server-env.sh",
  
  # Deployment docs
  "docs/deployment",
  
  # Database scripts
  "scripts/database",
  
  # Essential docs
  "docs/AI_CONTEXT.md",
  "docs/REMOTE_AI_README.md",
  "README.md"
)

# Copy files
Write-Host "`n[copy] Copying deployment files..." -ForegroundColor Cyan
$copiedCount = 0

foreach ($item in $FilesToCopy) {
  $sourcePath = Join-Path $ProjectRoot $item
  $destPath = Join-Path $PackageDir $item
  
  if (-not (Test-Path $sourcePath)) {
    Write-Host "  [skip] Not found: $item" -ForegroundColor Yellow
    continue
  }
  
  # Create parent directory if needed
  $destParent = Split-Path $destPath -Parent
  if (-not (Test-Path $destParent)) {
    New-Item -Path $destParent -ItemType Directory -Force | Out-Null
  }
  
  if (Test-Path $sourcePath -PathType Container) {
    # Copy directory
    Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
    Write-Host "  [ok] Copied directory: $item" -ForegroundColor Gray
  } else {
    # Copy file
    Copy-Item -Path $sourcePath -Destination $destPath -Force
    Write-Host "  [ok] Copied file: $item" -ForegroundColor Gray
  }
  $copiedCount++
}

# Copy frontend build if requested
if ($IncludeFrontendBuild) {
  $frontendDist = Join-Path $ProjectRoot "frontend\dist"
  if (Test-Path $frontendDist) {
    $destDist = Join-Path $PackageDir "frontend\dist"
    Copy-Item -Path $frontendDist -Destination $destDist -Recurse -Force
    Write-Host "  [ok] Copied frontend build: frontend/dist" -ForegroundColor Gray
    $copiedCount++
  } else {
    Write-Host "  [warn] Frontend build not found. Run 'npm run build' first." -ForegroundColor Yellow
  }
}

# Create .env template
Write-Host "`n[create] Creating .env template..." -ForegroundColor Cyan
$envTemplate = Join-Path $PackageDir ".env.example"
$envContent = @"
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=blue_user
DB_PASSWORD=your_secure_password_here
DB_NAME=blue_album

# JWT Configuration
SECRET_KEY=your_secret_key_here_minimum_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:8080

# Server Configuration
HOST=0.0.0.0
PORT=8000
"@
$envContent | Out-File -FilePath $envTemplate -Encoding UTF8 -Force
Write-Host "  [ok] Created .env.example" -ForegroundColor Gray

# Create deployment README
Write-Host "`n[create] Creating deployment README..." -ForegroundColor Cyan
$deployReadme = Join-Path $PackageDir "DEPLOYMENT_README.md"
$readmeContent = @"
# Blue Local Deployment Package

Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Package Contents

This package contains all files needed to deploy the Blue Local application.

### Directory Structure

\`\`\`
deployment-package/
├── backend/                 # Backend Python code
├── frontend/                # Frontend Vue.js code
│   ├── src/                # Source files
│   ├── public/             # Static assets
│   └── dist/               # Built files (if included)
├── nginx/                   # Nginx configuration
├── scripts/                 # Deployment scripts
│   ├── deployment/         # Deploy scripts
│   └── database/           # Database migration scripts
├── docs/                    # Documentation
│   └── deployment/         # Deployment guides
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose config
├── .env.example            # Environment variables template
└── DEPLOYMENT_README.md    # This file
\`\`\`

## Quick Start

### Option 1: Docker Deployment (Recommended)

\`\`\`bash
# 1. Copy package to server
scp -r deployment-package/ user@server:/path/to/destination/

# 2. On server, navigate to package directory
cd /path/to/destination/deployment-package/

# 3. Copy and configure environment
cp .env.docker.example .env.docker
nano .env.docker  # Edit configuration

# 4. Run deployment script
chmod +x scripts/deployment/deploy-docker.sh
./scripts/deployment/deploy-docker.sh
\`\`\`

### Option 2: Traditional Deployment

\`\`\`bash
# 1. Copy package to server
scp -r deployment-package/ user@server:/var/www/blue-local/

# 2. On server, navigate to package directory
cd /var/www/blue-local/

# 3. Copy and configure environment
cp .env.example .env
nano .env  # Edit configuration

# 4. Run deployment script
chmod +x scripts/deployment/deploy.sh
./scripts/deployment/deploy.sh
\`\`\`

## Pre-deployment Checklist

- [ ] MySQL 8.0+ installed and running
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed (for frontend build)
- [ ] Nginx installed (for traditional deployment)
- [ ] Docker & Docker Compose installed (for Docker deployment)
- [ ] Ports available: 3306 (MySQL), 8000 (Backend), 80/443 (Nginx)
- [ ] Domain name configured (if using HTTPS)

## Configuration

### Required Environment Variables

Edit \`.env\` or \`.env.docker\`:

- \`DB_HOST\`: MySQL host (default: localhost)
- \`DB_USER\`: MySQL username
- \`DB_PASSWORD\`: MySQL password (use strong password!)
- \`DB_NAME\`: Database name (default: blue_album)
- \`SECRET_KEY\`: JWT secret (min 32 characters)
- \`CORS_ORIGINS\`: Allowed frontend origins

## Post-deployment

After successful deployment:

1. Access the application:
   - Frontend: http://your-domain/ or http://server-ip/
   - Backend API: http://your-domain/api/ or http://server-ip:8000/
   - API Docs: http://your-domain/api/docs or http://server-ip:8000/docs

2. Create admin user:
   \`\`\`bash
   python scripts/database/create_admin_user.py
   \`\`\`

3. Test the application:
   - Login with admin credentials
   - Create a test post
   - Test file upload
   - Test sync room feature

## Troubleshooting

See \`docs/deployment/\` for detailed guides:
- \`服务器部署指南.md\` - Complete deployment guide
- \`部署检查清单.md\` - Pre-deployment checklist
- \`多种部署方案完整指南.md\` - Multiple deployment options

## Support

For issues or questions:
1. Check deployment documentation in \`docs/deployment/\`
2. Review logs: \`docker-compose logs\` or \`journalctl -u blue-local\`
3. Verify environment configuration
4. Check server environment: \`./scripts/deployment/check-server-env.sh\`

---

Generated by: \`scripts/deployment/collect-deployment-files.ps1\`
"@
$readmeContent | Out-File -FilePath $deployReadme -Encoding UTF8 -Force
Write-Host "  [ok] Created DEPLOYMENT_README.md" -ForegroundColor Gray

# Create file list
Write-Host "`n[create] Creating file list..." -ForegroundColor Cyan
$fileListPath = Join-Path $PackageDir "FILE_LIST.txt"
$fileList = Get-ChildItem -Path $PackageDir -Recurse -File | 
  ForEach-Object { $_.FullName.Replace($PackageDir + "\", "") } |
  Sort-Object
$fileList | Out-File -FilePath $fileListPath -Encoding UTF8 -Force
Write-Host "  [ok] Created FILE_LIST.txt ($($fileList.Count) files)" -ForegroundColor Gray

# Calculate package size
$packageSize = (Get-ChildItem -Path $PackageDir -Recurse -File | 
  Measure-Object -Property Length -Sum).Sum / 1MB

# Summary
Write-Host "`n[done] Deployment package created!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "  Location: $PackageDir" -ForegroundColor Cyan
Write-Host "  Files copied: $copiedCount items" -ForegroundColor Cyan
Write-Host "  Total files: $($fileList.Count)" -ForegroundColor Cyan
Write-Host "  Package size: $([math]::Round($packageSize, 2)) MB" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Write-Host "`n[next] Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review DEPLOYMENT_README.md in package directory" -ForegroundColor Gray
Write-Host "  2. Compress package: Compress-Archive -Path '$OutputDir' -DestinationPath 'blue-local-deploy.zip'" -ForegroundColor Gray
Write-Host "  3. Upload to server: scp blue-local-deploy.zip user@server:/path/" -ForegroundColor Gray
Write-Host "  4. Extract and deploy: unzip blue-local-deploy.zip && cd $OutputDir" -ForegroundColor Gray
