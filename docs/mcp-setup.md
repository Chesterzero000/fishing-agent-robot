# MCP 配置指南

本文档说明如何配置项目中需要的各种 MCP 服务器。

## 目录

- [MySQL MCP](#mysql-mcp)
- [Filesystem MCP](#filesystem-mcp)
- [Web Search MCP](#web-search-mcp)
- [Firecrawl MCP](#firecrawl-mcp)
- [自定义 Image MCP](#自定义-image-mcp)

---

## MySQL MCP

### 用途

连接 NAS 上的 MySQL 数据库，用于存储和查询知识点、发布记录等数据。

### 安装

```bash
npm install -g @modelcontextprotocol/server-mysql
```

### 配置

在 Claude Code 的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-mysql"
      ],
      "env": {
        "MYSQL_HOST": "192.168.1.79",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "fishing",
        "MYSQL_PASSWORD": "liu.ccit-1244",
        "MYSQL_DATABASE": "fishing"
      }
    }
  }
}
```

### 测试连接

在 Claude Code 中运行：

```
Use MySQL MCP to run: SELECT COUNT(*) FROM knowledge_points;
```

---

## Filesystem MCP

### 用途

读写 Obsidian 知识库中的 Markdown 文件，实现本地知识管理与数据库同步。

### 配置

在 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "Z:\\008.钓鱼教练Agent\\知识图谱\\Sustech钓鱼协会"
      ]
    }
  }
}
```

### 使用示例

```bash
# 读取知识库文件
Read filesystem MCP: /01-基础知识/钓具装备/鱼竿.md

# 创建新的知识点文件
Write to filesystem MCP: /01-基础知识/钓具装备/浮漂.md
```

---

## Web Search MCP

### 用途

搜索网络上的钓鱼知识内容，用于知识采集和素材获取。

### 配置

需要先获取搜索 API Key（推荐使用 Brave Search API）：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key_here"
      }
    }
  }
}
```

### 获取 Brave Search API Key

1. 访问 https://brave.com/search/api/
2. 注册账号
3. 创建 API Key（免费版每月 2000 次调用）

---

## Firecrawl MCP

### 用途

爬取网页内容，提取结构化知识。

### 安装

```bash
npm install -g @modelcontextprotocol/server-firecrawl
```

### 配置

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-firecrawl"
      ],
      "env": {
        "FIRECRAWL_API_KEY": "your_firecrawl_api_key_here"
      }
    }
  }
}
```

### 获取 Firecrawl API Key

1. 访问 https://www.firecrawl.dev/
2. 注册账号
3. 获取 API Key

---

## 自定义 Image MCP

### 用途

调用 Gemini API 生成小沄漫画图片。

### 方案选择

由于官方 MCP 暂不直接支持 Gemini，有以下方案：

#### 方案 A：使用 DALL-E MCP（替代方案）

```json
{
  "mcpServers": {
    "imagegen": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-imagegen"
      ],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

#### 方案 B：自建 Python MCP Server

创建 `mcp-servers/gemini-image/src/index.ts`：

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "gemini-image-server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "generate_image",
        description: "Generate image using Gemini API",
        inputSchema: {
          type: "object",
          properties: {
            prompt: {
              type: "string",
              description: "Image generation prompt",
            },
          },
          required: ["prompt"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "generate_image") {
    const prompt = request.params.arguments?.prompt as string;

    // Call Gemini API here
    // ...
    return {
      content: [
        {
          type: "text",
          text: `Image generated for: ${prompt}`,
        },
      ],
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

---

## 完整配置文件示例

将以下内容添加到 Claude Code 的配置文件（通常在 `~/.config/claude-code/mcp_config.json`）：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "192.168.1.79",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "fishing",
        "MYSQL_PASSWORD": "liu.ccit-1244",
        "MYSQL_DATABASE": "fishing"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "Z:\\008.钓鱼教练Agent\\知识图谱\\Sustech钓鱼协会"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key_here"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

---

## 配置步骤清单

- [ ] 1. 安装 Node.js（如果未安装）
- [ ] 2. 获取 Brave Search API Key
- [ ] 3. 获取 Firecrawl API Key（可选）
- [ ] 4. 配置 MySQL MCP
- [ ] 5. 配置 Filesystem MCP
- [ ] 6. 配置 Web Search MCP
- [ ] 7. 测试所有 MCP 连接
- [ ] 8. 运行数据库初始化脚本

---

## 故障排查

### MySQL 连接失败

1. 检查 NAS 是否开机
2. 确认 IP 地址和端口
3. 测试连接：`telnet 192.168.1.79 3306`

### Filesystem MCP 无法访问

1. 检查路径是否正确
2. Windows 使用 `\\` 代替 `\`
3. 确认 Obsidian 知识库路径存在

### Web Search 无结果

1. 确认 API Key 有效
2. 检查 API 配额是否用完
3. 尝试不同的搜索关键词
