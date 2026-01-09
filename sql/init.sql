-- Fishing Agent Robot - 数据库初始化脚本
-- 南科大钓鱼协会自动化内容创作系统

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS fishing DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fishing;

-- ============================================
-- 知识点表
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_points (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    title VARCHAR(200) NOT NULL COMMENT '知识点标题',
    category VARCHAR(50) NOT NULL COMMENT '分类：台钓/路亚/基础/进阶等',
    difficulty ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度等级',
    content TEXT NOT NULL COMMENT '知识内容',
    tags JSON COMMENT '标签数组',
    source_url VARCHAR(500) COMMENT '来源链接',
    obsidian_path VARCHAR(300) COMMENT 'Obsidian 文件路径',
    is_published BOOLEAN DEFAULT FALSE COMMENT '是否已发布',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    INDEX idx_published (is_published),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识点表';

-- ============================================
-- 发布记录表
-- ============================================
CREATE TABLE IF NOT EXISTS publish_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    knowledge_id INT NOT NULL COMMENT '关联知识点ID',
    platform ENUM('wechat', 'xiaohongshu') NOT NULL COMMENT '发布平台',
    title VARCHAR(200) NOT NULL COMMENT '发布标题',
    content TEXT NOT NULL COMMENT '发布内容',
    image_urls JSON COMMENT '图片链接数组',
    comic_script JSON COMMENT '漫画脚本',
    publish_date DATE COMMENT '发布日期',
    status ENUM('draft', 'pending', 'published', 'rejected') DEFAULT 'draft' COMMENT '状态',
    published_url VARCHAR(500) COMMENT '发布后链接',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (knowledge_id) REFERENCES knowledge_points(id) ON DELETE CASCADE,
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_publish_date (publish_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发布记录表';

-- ============================================
-- 知识采集源表
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_sources (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(100) NOT NULL COMMENT '来源名称',
    type ENUM('website', 'video', 'article', 'book') NOT NULL COMMENT '来源类型',
    url VARCHAR(500) COMMENT '链接地址',
    description TEXT COMMENT '描述',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识采集源表';

-- ============================================
-- 用户会话表（可选，用于多用户场景）
-- ============================================
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    session_id VARCHAR(100) UNIQUE NOT NULL COMMENT '会话ID',
    user_data JSON COMMENT '用户数据',
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后活动时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户会话表';

-- ============================================
-- 插入示例数据
-- ============================================

-- 插入知识采集源
INSERT INTO knowledge_sources (name, type, url, description) VALUES
('钓鱼之家', 'website', 'https://www.diaoyuzhijia.com', '钓鱼资讯、技巧分享社区'),
('路亚之家', 'website', 'https://www.lurehome.com', '路亚钓鱼专业社区'),
('化氏钓具公众号', 'article', NULL, '专业台钓知识分享'),
('B站钓鱼区', 'video', NULL, '钓鱼视频教程平台');

-- 插入首批知识点（模板）
INSERT INTO knowledge_points (title, category, difficulty, content, tags) VALUES
('认识你的第一根鱼竿', '基础', 'beginner',
'## 鱼竿的基本构成

鱼竿是钓鱼最基础的装备，主要由以下几个部分组成：

### 1. 竿身
- **材质**：碳纤维、玻璃纤维
- **调性**：硬调、中调、软调
- **长度**：2.7m、3.6m、4.5m、5.4m、6.3m等

### 2. 竿稍
- 竿的最顶端，连接鱼线
- 需要柔软但有一定强度

### 3. 握把
- 方便握持的部分
- 长节竿通常有EVA发泡握把

## 新手选竿建议

1. **材质选择**：建议选碳纤维竿，轻便且强度高
2. **长度选择**：新手推荐3.6m或4.5m，适合大多数场景
3. **调性选择**：建议中调，既能感知信号又容易操作
4. **价位选择**：入门竿100-300元即可，不要追求过高配置

## 使用注意事项

- 避免与硬物碰撞
- 收竿时注意擦干净
- 存放时保持干燥',
'["钓具", "入门", "鱼竿"]'),

('淡水常见鱼种识别', '基础', 'beginner',
'## 常见淡水鱼种

### 1. 鲫鱼
- **体型**：中小型，通常100-500g
- **特征**：身体侧扁，背部青灰色，腹部银白色
- **习性**：底层鱼类，杂食性
- **四季可钓**

### 2. 鲤鱼
- **体型**：中大型，常见500-3000g
- **特征**：身体圆筒形，有须，鳞片大
- **习性**：底层鱼类，荤素兼食
- **喜群游**

### 3. 草鱼
- **体型**：大型，常见1000-5000g
- **特征**：身体圆筒形，背部青灰色
- **习性**：中下层，草食性
- **力气大，遛鱼有趣**

### 4. 鲢鱼（白鲢）
- **体型**：中大型
- **特征**：身体侧扁，鳞片细小，银白色
- **习性**：中上层，滤食性
- **适合浮钓**

### 5. 鳙鱼（花鲢/胖头鱼）
- **体型**：大型
- **特征**：头大，身体暗黑色斑点
- **习性**：中上层，滤食性
- **性情温和']

## 鱼种识别要点

1. **看体型**：扁平型（鲫/鲢）vs 圆筒型（鲤/草）
2. **看颜色**：银白（鲫/鲢）vs 青灰（草/鲤）
3. **看胡须**：有须（鲤/草）vs 无须（鲫/鲢）
4. **看嘴巴**：上位（鲢/鳙）vs 端位（鲫/鲤/草）',
'["鱼种", "入门", "识别"]'),

('调漂入门：调四钓二', '台钓', 'intermediate',
'## 什么是调四钓二

调四钓二是台钓中最经典的调漂方法：

- **调四**：空钩半水调漂，让浮漂露出水面4目
- **钓二**：挂饵后调整浮漂位置，让浮漂露出水面2目

## 操作步骤

### 第一步：重铅找底
1. 挂重铅，浮漂下沉
2. 向上推浮漂直到露出水面
3. 此时铅坠到底，确认水深

### 第二步：调四
1. 下推浮漂（约子线长度+30cm）
2. 修剪铅皮，直到浮漂露出4目
3. 此时双钩悬浮

### 第三步：钓二
1. 挂上饵料
2. 向上推浮漂，直到露出2目
3. 此时可以开始垂钓

## 原理解析

- **调四时**：双钩悬浮，状态最灵敏
- **挂饵后**：饵料重量压下2目，浮漂露出2目
- **钓2目时**：上钩触底/轻触底，下钩躺底
- **鱼吸食**：浮漂上浮或下顿，信号明显

## 适用场景

- 野钓鲫鱼
- 钓鱼情温和时
- 水底较平时

## 注意事项

- 水深不足1米时不适用
- 走水严重时不适用
- 饵料太重时需要调整',
'["台钓", "调漂", "技巧"]'),

('路亚拟饵入门', '路亚', 'beginner',
'## 路亚拟饵分类

### 1. 软饵（Soft Lure）
- **类型**：虫型、鱼型、虾型
- **材质**：硅胶、软塑料
- **优点**：动作自然，鱼不易警觉
- **适合**：淡水、海水均可

### 2. 硬饵（Hard Lure）
- **米诺（Minnow）**：模仿小鱼，适合中层搜索
- **亮片（Spoon）**：反光诱鱼，适合远投
- **波趴（Popper）**：水面系，制造水花声
- **复合亮片（Spinnerbait）**：防挂底，搜索面积大

### 3. 铁板（Jig）
- **远投利器**：重量大，投得远
- **快搜快鱼**：适合钓海鱼、翘嘴等
- **需要配合铅头钩使用**

## 新手拟饵推荐

| 目标鱼种 | 推荐拟饵 | 颜色选择 |
|---------|---------|---------|
| 鲈鱼/翘嘴 | 米诺3-5cm | 银色/金色 |
| 鳟鱼 | 亮片 | 银色/彩色 |
| 黑鱼/鲈鱼 | 软虫 + 铅头钩 | 黑色/紫色 |
| 海鱼 | 铁板20-40g | 荧光色 |

## 操作技巧

### 收线技巧
- **匀速回收**：适合米诺、亮片
- **抽停**：抽一下停一下，模仿受伤小鱼
- **跳底**：软饵在水底跳动

### 技巧选择
- **活性高时**：快收、大动作
- **活性低时**：慢收、小动作',
'["路亚", "拟饵", "入门"]');

-- ============================================
-- 创建视图：待发布知识点
-- ============================================
CREATE OR REPLACE VIEW v_unpublished_knowledge AS
SELECT
    id,
    title,
    category,
    difficulty,
    SUBSTRING(content, 1, 200) as preview,
    tags,
    created_at
FROM knowledge_points
WHERE is_published = FALSE
ORDER BY created_at ASC;

-- ============================================
-- 创建视图：发布统计
-- ============================================
CREATE OR REPLACE VIEW v_publish_stats AS
SELECT
    DATE(publish_date) as date,
    platform,
    COUNT(*) as count,
    SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published_count
FROM publish_records
WHERE publish_date IS NOT NULL
GROUP BY DATE(publish_date), platform;

-- ============================================
-- 完成提示
-- ============================================
SELECT 'Database initialized successfully!' as status;
SELECT COUNT(*) as knowledge_count FROM knowledge_points;
SELECT COUNT(*) as source_count FROM knowledge_sources;
