#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小沄漫画生成脚本
根据知识点自动生成 6 格科普漫画
"""

import os
import sys
import json
from nano_banana_client import NanoBananaClient, XiaoyunComicGenerator, HostType


def generate_comic_from_knowledge(knowledge_topic: str, knowledge_content: str = None):
    """
    根据知识点生成漫画场景
    
    Args:
        knowledge_topic: 知识点主题
        knowledge_content: 知识点详细内容（可选）
    """
    # 这里可以根据知识点内容智能生成 6 个场景
    # 目前使用模板，后续可以接入 LLM 来生成场景描述
    
    # 示例场景模板
    scenes = [
        f"小沄遇到了关于{knowledge_topic}的问题，感到困惑",
        f"小沄开始学习{knowledge_topic}的知识，认真观察和学习",
        f"小沄发现了{knowledge_topic}的关键要点，恍然大悟",
        f"小沄按照学到的{knowledge_topic}方法进行实践操作",
        f"小沄在实践{knowledge_topic}时遇到了一个小挑战",
        f"小沄成功掌握了{knowledge_topic}，非常开心和满足"
    ]
    
    return scenes


def main():
    """主函数"""
    # 检查 API Key
    api_key = os.getenv("NANO_BANANA_API_KEY")
    if not api_key:
        print("错误：请设置环境变量 NANO_BANANA_API_KEY")
        print("\nWindows PowerShell:")
        print('  $env:NANO_BANANA_API_KEY = "your_api_key"')
        print("\nLinux/Mac:")
        print('  export NANO_BANANA_API_KEY="your_api_key"')
        sys.exit(1)
    
    # 选择 Host（默认国内直连，更快）
    host_type = HostType.DOMESTIC
    if "--overseas" in sys.argv:
        host_type = HostType.OVERSEAS
        print("使用海外 Host...")
    
    # 创建客户端和生成器
    print("初始化 Nano Banana 客户端...")
    client = NanoBananaClient(api_key=api_key, host_type=host_type)
    generator = XiaoyunComicGenerator(client)
    
    # 获取知识点（从命令行参数或使用示例）
    if len(sys.argv) > 1 and sys.argv[1] not in ["--overseas", "--help"]:
        topic = sys.argv[1]
    else:
        # 默认示例：调漂技巧
        topic = "调漂技巧"
        print(f"\n使用示例主题：{topic}")
        print("你可以传入自定义主题，例如：")
        print('  python generate_xiaoyun_comic.py "开饵技巧"')
    
    print(f"\n准备生成关于「{topic}」的 6 格漫画...")
    
    # 生成场景描述
    scenes = generate_comic_from_knowledge(topic)
    
    print("\n6 个场景：")
    for i, scene in enumerate(scenes, 1):
        print(f"  第{i}格：{scene}")
    
    # 询问确认
    if "--yes" not in sys.argv:
        confirm = input("\n确认生成？(y/n): ")
        if confirm.lower() != 'y':
            print("已取消")
            sys.exit(0)
    
    # 生成漫画
    try:
        print("\n开始生成漫画（这可能需要几分钟）...\n")
        results = generator.generate_6panel_comic(
            story_scenes=scenes,
            model="nano-banana-fast",  # 可以使用 nano-banana-pro 获得更高质量
            aspect_ratio="1:1"  # 1:1 适合单格，也可以改为 3:2
        )
        
        print("\n✓ 所有格子生成完成！")
        
        # 保存图片
        output_dir = f"./comic_output/{topic}"
        saved_files = generator.save_comic_images(results, output_dir=output_dir)
        
        print(f"\n✓ 所有图片已保存到: {output_dir}")
        print(f"✓ 共生成 {len(saved_files)} 张图片")
        
        # 保存元数据
        metadata = {
            "topic": topic,
            "scenes": scenes,
            "results": [
                {
                    "panel": i + 1,
                    "image_url": r.get("results", [{}])[0].get("url", ""),
                    "content": r.get("results", [{}])[0].get("content", ""),
                    "status": r.get("status", "")
                }
                for i, r in enumerate(results)
            ]
        }
        
        metadata_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"✓ 元数据已保存: {metadata_path}")
        
    except Exception as e:
        print(f"\n✗ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("小沄漫画生成工具")
        print("\n使用方法：")
        print('  python generate_xiaoyun_comic.py [知识点主题] [选项]')
        print("\n选项：")
        print("  --overseas    使用海外 Host（默认使用国内直连）")
        print("  --yes         跳过确认，直接生成")
        print("  --help        显示帮助信息")
        print("\n示例：")
        print('  python generate_xiaoyun_comic.py "调漂技巧"')
        print('  python generate_xiaoyun_comic.py "开饵方法" --overseas')
        print("\n环境变量：")
        print("  NANO_BANANA_API_KEY    Nano Banana API 密钥（必需）")
        sys.exit(0)
    
    main()

