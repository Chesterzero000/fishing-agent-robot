# Nano Banana API 集成使用指南

## 概述

本模块集成了 Nano Banana 图片生成 API，用于生成小沄的 6 格科普漫画。

## 功能特性

- ✅ 支持 Nano Banana 图片生成 API
- ✅ 支持流式响应和回调两种方式
- ✅ 支持国内直连和海外两种 Host
- ✅ 专门优化的小沄角色提示词
- ✅ 一键生成 6 格漫画
- ✅ 自动下载和保存图片

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置 API Key

### Windows PowerShell

```powershell
$env:NANO_BANANA_API_KEY = "your_api_key_here"
```

### Windows CMD

```cmd
set NANO_BANANA_API_KEY=your_api_key_here
```

### Linux/Mac

```bash
export NANO_BANANA_API_KEY="your_api_key_here"
```

## 使用方法

### 方法 1：使用便捷脚本生成 6 格漫画

```bash
# 使用默认主题（调漂技巧）
python generate_xiaoyun_comic.py

# 指定主题
python generate_xiaoyun_comic.py "开饵技巧"

# 使用海外 Host
python generate_xiaoyun_comic.py "路亚装备选择" --overseas

# 跳过确认直接生成
python generate_xiaoyun_comic.py "调漂技巧" --yes
```

### 方法 2：在代码中使用 API 客户端

```python
from nano_banana_client import NanoBananaClient, XiaoyunComicGenerator, HostType
import os

# 初始化客户端
api_key = os.getenv("NANO_BANANA_API_KEY")
client = NanoBananaClient(api_key=api_key, host_type=HostType.DOMESTIC)

# 创建漫画生成器
generator = XiaoyunComicGenerator(client)

# 生成单格漫画
result = generator.generate_single_panel(
    scene_description="小沄正在学习如何调漂",
    panel_number=1,
    aspect_ratio="1:1"
)
print(f"图片 URL: {result['results'][0]['url']}")

# 生成 6 格漫画
scenes = [
    "小沄第一次去钓鱼，对一切都很好奇",
    "小沄开始学习如何抛竿",
    "小沄发现了调漂的重要性",
    "小沄按照学到的方法实践",
    "小沄遇到了一点困难",
    "小沄终于成功了，非常开心"
]

results = generator.generate_6panel_comic(scenes)
generator.save_comic_images(results, output_dir="./comic_output")
```

### 方法 3：使用流式响应

```python
from nano_banana_client import NanoBananaClient, HostType

client = NanoBananaClient(api_key="your_key", host_type=HostType.DOMESTIC)

# 流式响应
for progress in client.generate_image(
    prompt="一只可爱的猫咪",
    stream=True
):
    print(f"进度: {progress.get('progress', 0)}%")
    if progress.get('status') == 'succeeded':
        print(f"图片 URL: {progress['results'][0]['url']}")
        break
```

### 方法 4：使用回调方式

```python
from nano_banana_client import NanoBananaClient, HostType

client = NanoBananaClient(api_key="your_key", host_type=HostType.DOMESTIC)

# 使用回调（需要提供 webhook URL）
result = client.generate_image(
    prompt="一只可爱的猫咪",
    webhook="https://your-domain.com/callback",
    stream=False
)

# 获取 task_id
task_id = result["data"]["id"]

# 轮询获取结果
final_result = client.wait_for_completion(task_id)
print(f"图片 URL: {final_result['results'][0]['url']}")
```

## API 参数说明

### NanoBananaClient.generate_image()

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | str | 必需 | 提示词 |
| model | str | "nano-banana-fast" | 模型名称（见下方模型列表） |
| aspect_ratio | str | "auto" | 图片比例（1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:4, 4:5, 21:9, auto） |
| image_size | str | "1K" | 图片大小（1K, 2K, 4K） |
| urls | List[str] | None | 参考图 URL 列表 |
| webhook | str | None | 回调地址 |
| shut_progress | bool | False | 是否关闭进度回复 |
| stream | bool | True | 是否使用流式响应 |

### 支持的模型

- `nano-banana-fast` - 快速生成（推荐日常使用）
- `nano-banana` - 标准模型
- `nano-banana-pro` - 专业版
- `nano-banana-pro-vt` - 专业版变体
- `nano-banana-pro-cl` - 专业版 CL
- `nano-banana-pro-vip` - VIP 版（支持 1K, 2K）
- `nano-banana-pro-4k-vip` - 4K VIP 版（仅支持 4K）

### XiaoyunComicGenerator 特性

- 自动生成符合小沄形象的提示词
- 根据格子编号自动调整表情和状态
- 支持批量生成 6 格漫画
- 自动下载和保存图片

## 输出文件结构

```
comic_output/
└── 知识点名称/
    ├── panel_1.png
    ├── panel_2.png
    ├── panel_3.png
    ├── panel_4.png
    ├── panel_5.png
    ├── panel_6.png
    └── metadata.json  # 包含场景描述、URL、状态等元数据
```

## 小沄形象设计规范

- **身体**：圆滚滚的荔枝形状，粉红色 (#E8A0A0)
- **头顶**：2-3 片小绿叶（荔枝蒂）
- **帽子**：橙色小火焰造型帽 (#F5A623)
- **表情**：极简风格，两个小黑点眼睛 + 小弧线嘴
- **四肢**：短短的小手小脚，简笔画风格
- **道具**：经常拿着一根小鱼竿
- **风格**：Chiikawa 风格，简单可爱

## 注意事项

1. **API Key 安全**：不要将 API Key 提交到代码仓库
2. **图片有效期**：生成的图片 URL 有效期为 2 小时，请及时下载
3. **生成时间**：分辨率越高，生成时间越长（1K 约 1-3 分钟，4K 可能需要更久）
4. **网络连接**：使用国内直连 Host 速度更快，但需要确保网络可以访问
5. **成本控制**：批量生成时注意 API 调用成本

## 错误处理

```python
try:
    result = generator.generate_single_panel("场景描述")
except Exception as e:
    print(f"生成失败: {e}")
    # 常见错误：
    # - API Key 无效
    # - 网络连接问题
    # - 提示词违规
    # - 任务超时
```

## 集成到工作流

在 `构想.md` 中提到的每日内容生成流程中，可以这样使用：

```python
# 在"6. 漫画生成"步骤
from generate_xiaoyun_comic import generate_comic_from_knowledge
from nano_banana_client import NanoBananaClient, XiaoyunComicGenerator

# 根据选定的知识点生成漫画
knowledge_point = "调漂技巧"
scenes = generate_comic_from_knowledge(knowledge_point)

# 生成 6 格漫画
client = NanoBananaClient(api_key=os.getenv("NANO_BANANA_API_KEY"))
generator = XiaoyunComicGenerator(client)
results = generator.generate_6panel_comic(scenes)

# 保存图片供后续使用
generator.save_comic_images(results, output_dir=f"./output/{knowledge_point}")
```

## 相关文档

- [构想.md](./构想.md) - 项目整体规划
- [Nano Banana API 文档](https://grsai.dakka.com.cn/docs) - 官方 API 文档

## 问题排查

1. **API 调用失败**
   - 检查 API Key 是否正确设置
   - 确认网络连接正常
   - 尝试切换 Host（国内/海外）

2. **图片生成时间过长**
   - 使用 `nano-banana-fast` 模型
   - 降低图片分辨率（1K）
   - 检查网络速度

3. **生成质量不理想**
   - 尝试使用 `nano-banana-pro` 模型
   - 优化提示词描述
   - 使用参考图（urls 参数）

