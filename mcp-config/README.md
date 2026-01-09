# MCP 配置文件说明

## 文件说明

- **mcp_config.json** - 模板配置文件（无敏感信息，可提交到 Git）
- **mcp_config.local.json** - 本地配置文件（包含你的实际 API Key，不会提交）
- **Claude Code 配置目录**: `~/.config/claude-code/` (Linux/Mac) 或 `%APPDATA%\claude-code\` (Windows)

## 安装步骤

### 方式一：使用本地配置文件（推荐）

**直接使用 `mcp_config.local.json`**，它已经包含了你的实际 API Key：

```powershell
# 复制本地配置文件到 Claude Code
Copy-Item mcp-config\mcp_config.local.json $env:APPDATA\claude-code\mcp_config.json
```

### 方式二：手动复制模板

1. **复制模板文件**
   ```powershell
   Copy-Item mcp-config\mcp_config.json $env:APPDATA\claude-code\mcp_config.json
   ```

2. **编辑配置文件，替换占位符**
   ```powershell
   notepad $env:APPDATA\claude-code\mcp_config.json
   ```
   - 将 `YOUR_GITHUB_TOKEN_HERE` 替换为你的实际 GitHub Token

3. **重启 Claude Code**

### 验证安装

在 Claude Code 中运行：

```
列出所有可用的 MCP 服务器
```

或使用工具测试：

```
使用 MySQL MCP 查询: SELECT COUNT(*) FROM knowledge_points;
```

## 配置项说明

### MySQL MCP
连接 NAS 上的 MySQL 数据库

| 参数 | 值 |
|------|-----|
| HOST | 192.168.1.79 |
| PORT | 3306 |
| USER | fishing |
| PASSWORD | liu.ccit-1244 |
| DATABASE | fishing |

### Filesystem MCP
访问 Obsidian 知识库

| 参数 | 值 |
|------|-----|
| PATH | Z:\\008.钓鱼教练Agent\\知识图谱\\Sustech钓鱼协会 |

### GitHub MCP
管理 GitHub 仓库（需要你的 GitHub Token）

| 参数 | 值 |
|------|-----|
| TOKEN | 需要替换为你的实际 Token |

### Brave Search MCP（暂未配置）
网络搜索功能（需要 Brave Search API Key）

| 参数 | 值 |
|------|-----|
| API KEY | 需要从 https://brave.com/search/api/ 获取 |

**注**：此服务暂时跳过，后续需要时可添加。

## 快速安装脚本

### PowerShell 脚本

将以下内容保存为 `install-mcp.ps1` 并运行：

```powershell
# MCP 配置安装脚本
$configPath = "$env:APPDATA\claude-code\mcp_config.json"
$sourceConfig = "mcp-config\mcp_config.json"

# 创建配置目录（如果不存在）
$configDir = Split-Path $configPath
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force
}

# 复制配置文件
Copy-Item -Path $sourceConfig -Destination $configPath -Force

Write-Host "MCP 配置已安装到: $configPath" -ForegroundColor Green
Write-Host "请重启 Claude Code 以使配置生效" -ForegroundColor Yellow
```

## 常见问题

### Q1: 配置后 MCP 服务器未启动

1. 检查配置文件路径是否正确
2. 确认 JSON 格式正确（无语法错误）
3. 查看 Claude Code 日志

### Q2: MySQL 连接失败

1. 确认 NAS 已开机
2. 测试连接：`telnet 192.168.1.79 3306`
3. 确认 MySQL 容器正在运行

### Q3: Filesystem MCP 无法访问

1. 确认 Obsidian 知识库路径存在
2. Windows 路径使用双反斜杠 `\\`
3. 检查文件权限

## 下一步

配置完成后，你可以：

1. **测试 MySQL 连接**
   ```
   使用 MySQL MCP 执行: SELECT * FROM knowledge_points LIMIT 5;
   ```

2. **初始化数据库**
   ```bash
   mysql -h 192.168.1.79 -P 3306 -u fishing -p fishing < sql/init.sql
   ```

3. **使用 Skills**
   ```
   /generate-post
   ```
