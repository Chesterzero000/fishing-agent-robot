#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SRT 字幕转 Markdown 笔记工具
使用智谱 AI API 进行转换
"""

import re
import sys
import os
from typing import List, Dict
import requests
import json

class SRTToMarkdown:
    def __init__(self, api_key: str = None):
        """
        初始化转换器
        
        Args:
            api_key: 智谱 AI API 密钥，如果为 None 则从环境变量 ZHIPU_API_KEY 读取
        """
        self.api_key = api_key or os.getenv('ZHIPU_API_KEY')
        if not self.api_key:
            raise ValueError("请设置智谱 API 密钥：通过参数传入或设置环境变量 ZHIPU_API_KEY")
        
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def parse_srt(self, srt_content: str) -> List[Dict]:
        """
        解析 SRT 字幕文件
        
        Args:
            srt_content: SRT 文件内容
            
        Returns:
            字幕条目列表，每个条目包含 {index, time, text}
        """
        # 移除 BOM 标记
        srt_content = srt_content.lstrip('\ufeff')
        
        # 按双换行符分割字幕块
        blocks = re.split(r'\n\s*\n', srt_content.strip())
        
        subtitles = []
        for block in blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            if len(lines) < 2:
                continue
            
            # 第一行是序号
            index = lines[0].strip()
            
            # 第二行是时间码
            timecode = lines[1].strip()
            
            # 剩余行是字幕文本
            text = '\n'.join(lines[2:]).strip()
            
            subtitles.append({
                'index': index,
                'time': timecode,
                'text': text
            })
        
        return subtitles
    
    def call_zhipu_api(self, prompt: str, model: str = "glm-4") -> str:
        """
        调用智谱 AI API
        
        Args:
            prompt: 提示词
            model: 模型名称，默认为 glm-4
            
        Returns:
            API 返回的文本内容
        """
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            raise Exception(f"API 调用失败: {str(e)}")
    
    def convert_to_markdown(self, srt_file: str, output_file: str = None, use_ai: bool = True) -> str:
        """
        将 SRT 文件转换为 Markdown
        
        Args:
            srt_file: SRT 文件路径
            output_file: 输出文件路径，如果为 None 则自动生成
            use_ai: 是否使用 AI 进行优化整理
            
        Returns:
            生成的 Markdown 内容
        """
        # 读取 SRT 文件
        with open(srt_file, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        # 解析字幕
        subtitles = self.parse_srt(srt_content)
        
        if not subtitles:
            raise ValueError("SRT 文件格式错误或为空")
        
        if use_ai:
            # 使用 AI 进行转换和优化
            print("正在使用智谱 AI 进行转换和优化...")
            
            # 构建提示词
            subtitle_text = "\n\n".join([
                f"[{sub['time']}] {sub['text']}"
                for sub in subtitles
            ])
            
            prompt = f"""请将以下字幕内容转换为结构化的 Markdown 笔记。

要求：
1. 提取关键信息和要点
2. 按照逻辑结构组织内容
3. 保留重要的时间戳信息
4. 使用合适的 Markdown 格式（标题、列表、引用等）
5. 去除重复和冗余内容
6. 添加适当的章节划分

字幕内容：
{subtitle_text}

请直接输出 Markdown 格式的笔记，不要添加额外的说明。"""
            
            markdown_content = self.call_zhipu_api(prompt)
        else:
            # 简单转换（不使用 AI）
            markdown_lines = ["# 字幕笔记\n\n"]
            for sub in subtitles:
                markdown_lines.append(f"## {sub['time']}\n\n")
                markdown_lines.append(f"{sub['text']}\n\n")
            markdown_content = "".join(markdown_lines)
        
        # 保存文件
        if output_file is None:
            output_file = srt_file.replace('.srt', '.md').replace('.SRT', '.md')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"转换完成！输出文件：{output_file}")
        return markdown_content


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：")
        print("  python srt_to_markdown.py <srt文件路径> [输出文件路径]")
        print("\n环境变量：")
        print("  设置 ZHIPU_API_KEY 环境变量来配置 API 密钥")
        print("\n示例：")
        print("  python srt_to_markdown.py video.srt")
        print("  python srt_to_markdown.py video.srt output.md")
        sys.exit(1)
    
    srt_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(srt_file):
        print(f"错误：文件不存在 - {srt_file}")
        sys.exit(1)
    
    try:
        converter = SRTToMarkdown()
        converter.convert_to_markdown(srt_file, output_file, use_ai=True)
    except Exception as e:
        print(f"错误：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()




