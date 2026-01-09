# NAS 常用命令参考

## 基本信息

| 项目 | 值 |
|------|-----|
| NAS IP | 192.168.1.79 |
| SSH 端口 | 25565 |
| SSH 用户 | 18587668166 |

## SSH 连接

### 基本连接
```bash
ssh -p 25565 18587668166@192.168.1.79
```

### 使用密钥连接（如果有）
```bash
ssh -p 25565 -i ~/.ssh/nas_key 18587668166@192.168.1.79
```

## Docker 容器管理

### 查看运行中的容器
```bash
docker ps
```

### 查看所有容器（包括停止的）
```bash
docker ps -a
```

### MySQL 容器操作

#### 查看容器状态
```bash
docker ps | grep fishing-mysql
```

#### 进入容器
```bash
docker exec -it fishing-mysql bash
```

#### 查看容器日志
```bash
docker logs fishing-mysql
```

#### 重启容器
```bash
docker restart fishing-mysql
```

### Neo4j 容器操作

#### 查看容器状态
```bash
docker ps | grep fishing-neo4j
```

#### 访问 Web 界面
```
http://192.168.1.79:7474
```

#### 重启容器
```bash
docker restart fishing-neo4j
```

### Redis 容器操作

#### 连接 Redis
```bash
docker exec -it redis redis-cli
```

#### 重启容器
```bash
docker restart redis
```

## MySQL 操作

### 从本地连接到 NAS MySQL
```bash
mysql -h 192.168.1.79 -P 3306 -u fishing -p fishing
```

### 导入 SQL 文件
```bash
mysql -h 192.168.1.79 -P 3306 -u fishing -p fishing < /path/to/file.sql
```

### 导出数据库
```bash
mysqldump -h 192.168.1.79 -P 3306 -u fishing -p fishing > backup.sql
```

### 常用 SQL 查询

```sql
-- 查看所有表
SHOW TABLES;

-- 查看知识点数量
SELECT COUNT(*) FROM knowledge_points;

-- 查看未发布的知识点
SELECT * FROM knowledge_points WHERE is_published = FALSE;

-- 查看最近的发布记录
SELECT * FROM publish_records ORDER BY created_at DESC LIMIT 10;
```

## 文件传输

### 从 NAS 下载文件
```bash
scp -P 25565 18587668166@192.168.1.79:/path/to/file ./
```

### 上传文件到 NAS
```bash
scp -P 25565 ./local-file 18587668166@192.168.1.79:/path/to/destination/
```

### 同步目录（rsync）
```bash
rsync -avz -e "ssh -p 25565" ./local-dir/ 18587668166@192.168.1.79:/remote-dir/
```

## 网络测试

### 测试 MySQL 连接
```bash
telnet 192.168.1.79 3306
# 或
nc -zv 192.168.1.79 3306
```

### 测试 Neo4j 连接
```bash
telnet 192.168.1.79 7474  # Web
telnet 192.168.1.79 7687  # Bolt
```

### 测试 Redis 连接
```bash
telnet 192.168.1.79 6379
```

## Obsidian 知识库路径

```
Z:\008.钓鱼教练Agent\知识图谱\Sustech钓鱼协会
```

## 故障排查

### NAS 无法连接
1. 检查 NAS 是否开机：`ping 192.168.1.79`
2. 检查网络连接
3. 确认 SSH 端口是否正确

### Docker 容器未运行
```bash
# 查看容器状态
docker ps -a

# 启动停止的容器
docker start fishing-mysql
docker start fishing-neo4j
docker start redis
```

### MySQL 连接失败
1. 检查容器是否运行：`docker ps | grep fishing-mysql`
2. 检查端口是否开放：`telnet 192.168.1.79 3306`
3. 查看容器日志：`docker logs fishing-mysql`

## 常用快捷命令

### 一键连接 SSH
```bash
# 可以添加到 ~/.bashrc 或创建别名
alias nas='ssh -p 25565 18587668166@192.168.1.79'
alias nas-mysql='mysql -h 192.168.1.79 -P 3306 -u fishing -p fishing'
```

### Windows PowerShell 别名
```powershell
# 添加到 $PROFILE
function nas { ssh -p 25565 18587668166@192.168.1.79 }
function nas-mysql { mysql -h 192.168.1.79 -P 3306 -u fishing -p fishing }
```

## 项目相关端口汇总

| 服务 | 端口 | 用途 |
|------|------|------|
| SSH | 25565 | 远程登录 |
| MySQL | 3306 | 数据库 |
| Neo4j Web | 7474 | 图数据库 Web 界面 |
| Neo4j Bolt | 7687 | 图数据库连接 |
| Redis | 6379 | 缓存 |
| fishing_agent | 8000 | Agent API |
