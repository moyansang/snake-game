# 贪吃蛇 - 一键 Git 初始化 & 上传 GitHub
$ErrorActionPreference = "Stop"
Set-Location "C:\Users\moyan\Desktop\贪吃蛇"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  贪吃蛇 - Git 上传工具" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. Git 配置
Write-Host "[1/5] 检查 Git..." -ForegroundColor Yellow
$git = "C:\Users\moyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe"
if (-not (Test-Path $git)) { $git = "git" }
& $git --version
Write-Host ""

# 2. 添加文件
Write-Host "[2/5] 添加文件..." -ForegroundColor Yellow
& $git add .
Write-Host ""

# 3. 提交
Write-Host "[3/5] 提交..." -ForegroundColor Yellow
& $git commit -m "feat: 贪吃蛇游戏 - 主菜单、倒计时、存档、音效、音量控制、设置"
Write-Host ""

# 4. 创建分支
Write-Host "[4/5] 设置分支..." -ForegroundColor Yellow
& $git branch -M main
Write-Host ""

# 5. 检查 gh CLI
Write-Host "[5/5] 检查 GitHub CLI..." -ForegroundColor Yellow
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue

if (-not $ghInstalled) {
    Write-Host ""
    Write-Host "⚠ GitHub CLI (gh) 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请执行以下步骤:" -ForegroundColor White
    Write-Host "  1. 安装 gh: https://cli.github.com/" -ForegroundColor Gray
    Write-Host "  2. 登录: gh auth login" -ForegroundColor Gray
    Write-Host "  3. 重新运行此脚本" -ForegroundColor Gray
    Write-Host ""
    Read-Host "按 Enter 退出"
    exit 0
}

# 检查登录状态
$authResult = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ 请先登录: gh auth login" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 0
}

# 创建仓库并推送
Write-Host "创建 GitHub 仓库..." -ForegroundColor Green
gh repo create moyansang/snake-game --public --source=. --remote=origin --push 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "仓库可能已存在, 尝试推送..." -ForegroundColor Yellow
    & $git remote add origin https://github.com/moyansang/snake-game.git 2>$null
    & $git push -u origin main
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  ✓ 完成! https://github.com/moyansang/snake-game" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Read-Host "按 Enter 退出"
