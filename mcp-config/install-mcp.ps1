# MCP 配置安装脚本
# 用于将 MCP 配置文件安装到 Claude Code 配置目录

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Fishing Agent Robot - MCP 配置安装  " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 获取项目根目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

# 配置文件路径
$configPath = "$env:APPDATA\claude-code\mcp_config.json"
$sourceConfig = Join-Path $scriptPath "mcp_config.json"

# 检查源配置文件是否存在
if (-not (Test-Path $sourceConfig)) {
    Write-Host "错误: 找不到配置文件 $sourceConfig" -ForegroundColor Red
    exit 1
}

# 创建配置目录（如果不存在）
$configDir = Split-Path $configPath
if (-not (Test-Path $configDir)) {
    Write-Host "创建配置目录: $configDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# 检查是否已有配置文件
if (Test-Path $configPath) {
    Write-Host "警告: 已存在配置文件 $configPath" -ForegroundColor Yellow
    $backupPath = "$configPath.backup"
    Write-Host "备份旧配置到: $backupPath" -ForegroundColor Yellow
    Copy-Item -Path $configPath -Destination $backupPath -Force
}

# 复制配置文件
Write-Host "安装 MCP 配置..." -ForegroundColor Green
Copy-Item -Path $sourceConfig -Destination $configPath -Force

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "配置文件位置: $configPath" -ForegroundColor White
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "1. 编辑配置文件，填入你的 GitHub Token 和 Brave API Key" -ForegroundColor White
Write-Host "2. 重启 Claude Code" -ForegroundColor White
Write-Host "3. 运行测试: 使用 MySQL MCP 查询数据库" -ForegroundColor White
Write-Host ""

# 询问是否打开配置文件进行编辑
$response = Read-Host "是否现在打开配置文件进行编辑? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    notepad $configPath
}

Write-Host ""
Write-Host "注意事项:" -ForegroundColor Yellow
Write-Host "- GitHub Token: 从 https://github.com/settings/tokens 生成" -ForegroundColor White
Write-Host "- Brave API Key: 从 https://brave.com/search/api/ 获取（免费2000次/月）" -ForegroundColor White
Write-Host ""
