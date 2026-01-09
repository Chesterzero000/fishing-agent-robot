# Claude Code 启动脚本（使用智谱 AI）
# 使用方法：在 PowerShell 中运行 .\start-claude.ps1

# 设置环境变量
$env:ANTHROPIC_AUTH_TOKEN = "7783a011749143cd95cf0ca55eef85d6.pYDyNJFGY0XjJ8uv"
$env:ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"
$env:ANTHROPIC_MODEL = "GLM-4.6"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "GLM-4.6"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "GLM-4.6"

# 刷新 PATH（确保能找到 claude 命令）
$env:Path += ";D:\Program Files (x86)\node"

Write-Host "正在启动 Claude Code（使用智谱 AI GLM-4.6）..." -ForegroundColor Green
Write-Host ""

# 启动 Claude Code
claude




