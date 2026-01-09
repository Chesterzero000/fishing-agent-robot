# Fishing Agent Robot

南科大钓鱼协会自动化内容创作系统

## 项目概述

利用 AI Agent、MCP 工具和 Skills 实现每日钓鱼知识科普内容的半自动生成，为南科大钓鱼协会的公众号和小红书账号提供内容支持。

## IP 形象：小沄

- **名字**：小沄（Xiao Yun）
- **身份**：南科大钓鱼协会吉祥物
- **外形**：圆滚滚的荔枝形状，粉红色，头顶绿叶，戴橙色火焰帽，手持小鱼竿

## 技术栈

- **AI**：Claude Code (Agent + Skills)
- **MCP 服务器**：
  - GitHub MCP（代码管理）
  - MySQL MCP（数据存储）
  - Filesystem MCP（Obsidian 集成）
  - Web Search MCP（知识采集）
  - Firecrawl MCP（网页爬取）
- **存储**：
  - MySQL（业务数据）
  - Neo4j（知识图谱）
  - Obsidian（知识库前端）
- **图像生成**：Gemini API

## 项目结构

```
├── skills/           # Agent Skills 定义
├── mcp-config/       # MCP 服务器配置
├── docs/            # 项目文档
├── scripts/         # 工具脚本
├── sql/             # 数据库脚本
└── README.md
```

## 快速开始

### 1. 配置 MCP 服务器

参考 [MCP 配置指南](./docs/mcp-setup.md)

### 2. 初始化数据库

```bash
# 连接到 NAS MySQL 并执行初始化脚本
mysql -h 192.168.1.79 -P 3306 -u fishing -p < sql/init.sql
```

### 3. 使用 Skills

```bash
# 生成今日推送内容
/daily-post

# 采集新知识
/collect-knowledge

# 生成双平台文案
/generate-copy
```

## 发布平台

| 平台 | 风格 | 更新频率 |
|------|------|----------|
| 公众号 | 正式、系统、硬核 | 每天 |
| 小红书 | 亲民、互动、轻松 | 每天 |

## 许可证

MIT License
