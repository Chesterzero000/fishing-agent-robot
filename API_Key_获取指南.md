# API Key 获取指南

本指南详细说明如何获取项目所需的两个 API Key。

---

## 1. GitHub Personal Access Token（GitHub 个人访问令牌）

### 用途
用于 GitHub MCP 服务器，让 AI Agent 能够访问和管理你的 GitHub 仓库（读取代码、创建 Issue、查看 PR 等）。

### 获取步骤

#### 步骤 1：登录 GitHub
1. 访问 [GitHub 官网](https://github.com)
2. 登录你的 GitHub 账号（如果没有账号，先注册）

#### 步骤 2：进入 Token 设置页面

**方法 1：直接链接（最简单）** ⭐ 推荐
直接点击这个链接，无需找菜单：
👉 **https://github.com/settings/tokens**

**方法 2：通过菜单导航**
1. 点击右上角头像
2. 选择 **Settings（设置）**
3. **重要**：在左侧菜单栏向下滚动到底部
4. 找到并点击 **Developer settings（开发者设置）**
   - 位置：在 Settings 侧边栏的最底部，在 "Archives" 下方
   - 如果看不到，继续向下滚动左侧菜单
5. 点击 **Personal access tokens（个人访问令牌）**
6. 点击 **Tokens (classic)** 或 **Fine-grained tokens**

**如果还是找不到**：
- 直接使用快速链接：https://github.com/settings/tokens
- 或者访问：https://github.com/settings/applications，然后点击左侧的 "Personal access tokens"

#### 步骤 3：创建新 Token
1. 点击 **Generate new token（生成新令牌）** → **Generate new token (classic)**
   - 如果看到的是细粒度令牌（Fine-grained token）页面，也可以使用，配置方法见下方

2. 填写 Token 信息：

   **如果是 Classic Token：**
   - **Note（备注）**：填写用途，例如 `MCP Server` 或 `钓鱼协会Agent`
   - **Expiration（过期时间）**：选择有效期（建议选择 `90 days` 或 `No expiration`）
   - **Select scopes（选择权限）**：勾选以下权限：
     - ✅ `repo` - 完整仓库访问权限（读取和写入代码）
     - ✅ `workflow` - 更新 GitHub Action 工作流
     - ✅ `read:org` - 读取组织信息（如果使用组织仓库）

   **如果是 Fine-grained Token（细粒度令牌）：**
   - **资源所有者（Resource Owner）**：保持默认（你的用户名）
   - **过期（Expiration）**：选择 "无过期" 或设置 90 天
   - **存储库访问（Repository Access）**：选择 **"所有存储库（All repositories）"**
   - **权限（Permissions）**：点击 **"+ 添加权限"** 按钮，添加以下权限：
     - ✅ **存储库权限（Repository permissions）**：
       - `Contents` - 设置为 **读写（Read and write）**
       - `Metadata` - 设置为 **只读（Read-only）**（通常已默认添加）
       - `Pull requests` - 设置为 **读写（Read and write）**（如果需要）
       - `Issues` - 设置为 **读写（Read and write）**（如果需要）
     - ✅ **Actions 权限**：
       - `Actions` - 设置为 **只读（Read-only）** 或 **读写（Read and write）**
     - ✅ **账号权限（Account permissions）**（如果需要访问组织）：
       - `Organization administration` - 设置为 **只读（Read-only）**

#### 步骤 4：生成并复制 Token
1. 滚动到页面底部，点击 **Generate token（生成令牌）**
2. ⚠️ **重要**：立即复制生成的 Token，它只显示一次！
   - Token 格式类似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
3. 将 Token 保存到安全的地方（如密码管理器）

### 验证 Token
在命令行测试：
```bash
# 测试 Token 是否有效
curl -H "Authorization: token YOUR_TOKEN_HERE" https://api.github.com/user
```

如果返回你的用户信息，说明 Token 有效。

---

## 2. Brave Search API Key

### 用途
用于 Web Search MCP 服务器，让 AI Agent 能够搜索互联网内容（采集钓鱼知识、查找资料等）。

### 获取步骤

#### 步骤 1：访问 Brave Search API 页面
直接访问：https://brave.com/search/api/

#### 步骤 2：注册/登录账号
1. 点击页面上的 **Sign up** 或 **Get started**
2. 如果没有账号，需要注册：
   - 填写邮箱
   - 设置密码
   - 验证邮箱

#### 步骤 3：创建 API Key
1. 登录后，进入 **Dashboard（控制台）**
2. 找到 **API Keys** 部分
3. 点击 **Create API Key** 或 **Generate New Key**
4. 填写 Key 名称（例如：`FishingAgent`）
5. 点击 **Create** 或 **Generate**

#### 步骤 4：复制 API Key
1. ⚠️ **重要**：立即复制生成的 API Key
   - Key 格式类似：`BSA_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. 保存到安全的地方

### 免费额度
- **免费套餐**：每月 2000 次搜索请求
- 对于每日内容创作来说，通常足够使用
- 如果需要更多，可以考虑付费套餐

### 验证 API Key
```bash
# 测试 API Key 是否有效
curl "https://api.search.brave.com/res/v1/web/search?q=test&key=YOUR_API_KEY_HERE"
```

如果返回搜索结果 JSON，说明 Key 有效。

---

## 3. 配置到项目中

### 方法 1：环境变量（推荐）

#### Windows PowerShell
```powershell
# 设置 GitHub Token
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 设置 Brave API Key
$env:BRAVE_API_KEY = "BSA_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### Windows CMD
```cmd
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
set BRAVE_API_KEY=BSA_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Linux/Mac
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export BRAVE_API_KEY="BSA_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 方法 2：配置文件
在 MCP 配置文件中替换占位符：

找到配置文件（通常是 `mcp_config.json` 或类似文件），替换：
```json
{
  "github": {
    "token": "YOUR_GITHUB_TOKEN_HERE"  → "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "brave": {
    "api_key": "YOUR_BRAVE_API_KEY_HERE"  → "BSA_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

## 4. 安全注意事项

### ✅ 安全做法
- [x] 使用环境变量而不是硬编码在代码中
- [x] 不要将 API Key 提交到 Git 仓库
- [x] 定期轮换 Token（GitHub Token 建议每 90 天更换一次）
- [x] 使用最小权限原则（只授予必要的权限）
- [x] 将 Token 保存在密码管理器中

### ❌ 避免的操作
- ❌ 不要在代码中直接写入 API Key
- ❌ 不要将包含 API Key 的文件上传到公共仓库
- ❌ 不要在聊天记录中分享 API Key
- ❌ 不要使用过长的有效期（除非必要）

---

## 5. 常见问题

### Q: GitHub Token 和 GitHub 密码有什么区别？
**A:** 
- **GitHub 密码**：用于登录 GitHub 网站
- **Personal Access Token**：用于程序访问 GitHub API，可以设置权限和有效期，更安全

### Q: 我的 GitHub Token 过期了怎么办？
**A:** 
1. 按照步骤 2-4 重新生成一个新 Token
2. 用新 Token 替换配置文件中的旧 Token
3. 旧 Token 会自动失效

### Q: Brave Search API 免费额度够用吗？
**A:** 
- 每天约 66 次搜索（2000 / 30）
- 对于每日内容创作工作流，通常足够
- 如果不够，可以：
  - 优化搜索策略（减少不必要的搜索）
  - 使用缓存机制
  - 考虑付费套餐

### Q: 我可以使用其他搜索引擎 API 吗？
**A:** 
可以，但需要修改 MCP 配置。常见替代方案：
- Google Custom Search API
- Bing Search API
- DuckDuckGo API（免费，但功能有限）

---

## 6. 快速检查清单

- [ ] 已获取 GitHub Personal Access Token
- [ ] 已获取 Brave Search API Key
- [ ] 已配置到环境变量或配置文件
- [ ] 已验证 API Key 有效
- [ ] 已保存 API Key 到安全位置
- [ ] 已检查 `.gitignore` 确保不会提交 API Key

---

## 7. 相关链接

- [GitHub Token 设置页面](https://github.com/settings/tokens)
- [Brave Search API 官网](https://brave.com/search/api/)
- [GitHub API 文档](https://docs.github.com/en/rest)
- [Brave Search API 文档](https://api.search.brave.com/)

---

**提示**：如果遇到问题，可以查看项目中的 `mcp-config/mcp_config.json` 配置文件，查看具体的配置格式要求。

