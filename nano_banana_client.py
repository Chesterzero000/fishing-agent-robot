#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nano Banana API 客户端
用于生成小沄漫画图片
"""

import os
import json
import time
import requests
from typing import List, Dict, Optional, Union, Iterator
from enum import Enum


class HostType(Enum):
    """API Host 类型"""
    OVERSEAS = "https://grsaiapi.com"  # 海外
    DOMESTIC = "https://grsai.dakka.com.cn"  # 国内直连


class NanoBananaClient:
    """Nano Banana API 客户端"""
    
    def __init__(self, api_key: str, host_type: HostType = HostType.DOMESTIC):
        """
        初始化客户端
        
        Args:
            api_key: API 密钥
            host_type: Host 类型，默认使用国内直连
        """
        self.api_key = api_key
        self.host = host_type.value
        self.base_url = f"{self.host}/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_image(
        self,
        prompt: str,
        model: str = "nano-banana-fast",
        aspect_ratio: str = "auto",
        image_size: str = "1K",
        urls: Optional[List[str]] = None,
        webhook: Optional[str] = None,
        shut_progress: bool = False,
        stream: bool = True
    ) -> Union[Dict, Iterator[Dict]]:
        """
        生成图片
        
        Args:
            prompt: 提示词
            model: 模型名称，默认 nano-banana-fast
            aspect_ratio: 图片比例，默认 auto
            image_size: 图片大小，默认 1K
            urls: 参考图 URL 列表（可选）
            webhook: 回调地址（可选）
            shut_progress: 是否关闭进度回复，默认 False
            stream: 是否使用流式响应，默认 True
            
        Returns:
            如果 stream=True：返回生成器，迭代返回进度和结果
            如果 stream=False：返回最终结果字典
        """
        url = f"{self.base_url}/draw/nano-banana"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
        }
        
        if urls:
            payload["urls"] = urls
        
        if webhook:
            payload["webHook"] = webhook
        elif not stream:
            # 如果不使用流式且没有 webhook，需要立即返回 id
            payload["webHook"] = "-1"
        
        if shut_progress:
            payload["shutProgress"] = True
        
        if stream and not webhook:
            # 流式响应
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            def _stream_generator():
                buffer = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        buffer += line
                        # 尝试解析 JSON（流式响应可能是多个 JSON 对象）
                        try:
                            # 处理 SSE 格式
                            if line.startswith("data: "):
                                json_str = line[6:]  # 移除 "data: " 前缀
                                if json_str.strip():
                                    yield json.loads(json_str)
                            else:
                                # 尝试直接解析
                                yield json.loads(line)
                        except json.JSONDecodeError:
                            # 可能是不完整的 JSON，继续累积
                            continue
                        buffer = ""
            
            return _stream_generator()
        else:
            # 非流式响应
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
    
    def get_result(self, task_id: str) -> Dict:
        """
        获取任务结果
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务结果字典
        """
        url = f"{self.base_url}/draw/result"
        payload = {"id": task_id}
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 300,
        poll_interval: int = 3
    ) -> Dict:
        """
        轮询等待任务完成
        
        Args:
            task_id: 任务 ID
            max_wait_time: 最大等待时间（秒），默认 300
            poll_interval: 轮询间隔（秒），默认 3
            
        Returns:
            最终结果字典
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            result = self.get_result(task_id)
            
            if result.get("code") == 0:
                data = result.get("data", {})
                status = data.get("status", "")
                
                if status == "succeeded":
                    return data
                elif status == "failed":
                    raise Exception(f"任务失败: {data.get('failure_reason', '')} - {data.get('error', '')}")
                # status == "running" 继续等待
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"任务超时: {task_id}")
    
    def generate_image_sync(
        self,
        prompt: str,
        model: str = "nano-banana-fast",
        aspect_ratio: str = "auto",
        image_size: str = "1K",
        urls: Optional[List[str]] = None,
        max_wait_time: int = 300
    ) -> Dict:
        """
        同步生成图片（内部使用轮询）
        
        Args:
            prompt: 提示词
            model: 模型名称
            aspect_ratio: 图片比例
            image_size: 图片大小
            urls: 参考图 URL 列表
            max_wait_time: 最大等待时间
            
        Returns:
            最终结果字典
        """
        # 使用 webHook="-1" 立即获取 task_id
        result = self.generate_image(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            urls=urls,
            webhook="-1",
            stream=False
        )
        
        if result.get("code") == 0:
            task_id = result["data"]["id"]
            return self.wait_for_completion(task_id, max_wait_time)
        else:
            raise Exception(f"创建任务失败: {result.get('msg', '')}")


class XiaoyunComicGenerator:
    """小沄漫画生成器"""
    
    def __init__(self, client: NanoBananaClient):
        """
        初始化生成器
        
        Args:
            client: NanoBananaClient 实例
        """
        self.client = client
    
    def get_xiaoyun_prompt(self, scene_description: str, panel_number: int = None) -> str:
        """
        生成小沄角色的提示词
        
        Args:
            scene_description: 场景描述
            panel_number: 格子编号（1-6），用于区分表情和状态
            
        Returns:
            完整的提示词
        """
        base_prompt = """一个可爱的吉祥物角色"小沄"：圆滚滚的荔枝形状身体，粉红色(#E8A0A0)，表面有荔枝凸起纹理。头顶有2-3片小绿叶（荔枝蒂）。戴着橙色小火焰造型帽(#F5A623，融入南科大校徽火炬元素)。极简风格的呆萌表情：两个小黑点眼睛 + 小弧线嘴。短短的小手小脚，简笔画风格。手里拿着一根小鱼竿。"""
        
        # 根据格子编号调整表情
        if panel_number:
            if panel_number == 1:
                emotion = "疑惑的表情，好奇地看着前方"
            elif panel_number == 2:
                emotion = "认真学习的样子，专注地观察"
            elif panel_number == 3:
                emotion = "惊讶的表情，发现了什么"
            elif panel_number == 4:
                emotion = "实践中的样子，认真操作"
            elif panel_number == 5:
                emotion = "遇到困难或惊喜，表情生动"
            elif panel_number == 6:
                emotion = "开心的表情，成功的样子"
            else:
                emotion = "呆萌可爱的表情"
        else:
            emotion = "呆萌可爱的表情"
        
        full_prompt = f"{base_prompt} {emotion}。{scene_description} Chiikawa风格的简单可爱插画，干净白色背景，全身视图，高质量，细节丰富。"
        
        return full_prompt
    
    def generate_single_panel(
        self,
        scene_description: str,
        panel_number: int = None,
        aspect_ratio: str = "1:1",
        model: str = "nano-banana-fast"
    ) -> Dict:
        """
        生成单格漫画
        
        Args:
            scene_description: 场景描述
            panel_number: 格子编号
            aspect_ratio: 图片比例，默认 1:1（适合单格）
            model: 模型名称
            
        Returns:
            生成结果字典
        """
        prompt = self.get_xiaoyun_prompt(scene_description, panel_number)
        
        print(f"正在生成第 {panel_number} 格漫画...")
        result = self.client.generate_image_sync(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            image_size="1K"
        )
        
        return result
    
    def generate_6panel_comic(
        self,
        story_scenes: List[str],
        model: str = "nano-banana-fast",
        aspect_ratio: str = "3:2"  # 适合 6 格漫画的比例
    ) -> List[Dict]:
        """
        生成 6 格漫画
        
        Args:
            story_scenes: 6 个场景描述的列表
            model: 模型名称
            aspect_ratio: 每格的图片比例，默认 3:2
            
        Returns:
            6 个格子的生成结果列表
        """
        if len(story_scenes) != 6:
            raise ValueError("需要提供 6 个场景描述")
        
        results = []
        
        for i, scene in enumerate(story_scenes, start=1):
            print(f"\n[{i}/6] 生成第 {i} 格...")
            try:
                result = self.generate_single_panel(
                    scene_description=scene,
                    panel_number=i,
                    aspect_ratio=aspect_ratio,
                    model=model
                )
                results.append(result)
                print(f"✓ 第 {i} 格生成完成")
            except Exception as e:
                print(f"✗ 第 {i} 格生成失败: {str(e)}")
                raise
        
        return results
    
    def save_comic_images(self, results: List[Dict], output_dir: str = "./comic_output"):
        """
        保存漫画图片
        
        Args:
            results: 生成结果列表
            output_dir: 输出目录
        """
        import os
        import urllib.request
        from pathlib import Path
        
        os.makedirs(output_dir, exist_ok=True)
        
        saved_files = []
        for i, result in enumerate(results, start=1):
            if result.get("results") and len(result["results"]) > 0:
                image_url = result["results"][0]["url"]
                filename = f"panel_{i}.png"
                filepath = os.path.join(output_dir, filename)
                
                print(f"正在下载第 {i} 格图片...")
                urllib.request.urlretrieve(image_url, filepath)
                saved_files.append(filepath)
                print(f"✓ 已保存: {filepath}")
        
        return saved_files


def main():
    """示例用法"""
    import sys
    
    # 从环境变量读取 API Key
    api_key = os.getenv("NANO_BANANA_API_KEY")
    if not api_key:
        print("错误：请设置环境变量 NANO_BANANA_API_KEY")
        print("\n使用方法：")
        print("  Windows PowerShell: $env:NANO_BANANA_API_KEY = 'your_api_key'")
        print("  Linux/Mac: export NANO_BANANA_API_KEY='your_api_key'")
        sys.exit(1)
    
    # 选择 Host（默认国内直连）
    host_type = HostType.DOMESTIC
    if "--overseas" in sys.argv:
        host_type = HostType.OVERSEAS
    
    # 创建客户端
    client = NanoBananaClient(api_key=api_key, host_type=host_type)
    generator = XiaoyunComicGenerator(client)
    
    # 示例：生成单格漫画
    if "--single" in sys.argv:
        scene = "小沄正在学习如何调漂，手里拿着浮漂仔细观察"
        result = generator.generate_single_panel(scene, panel_number=1)
        print("\n生成结果：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 保存图片
        if result.get("results"):
            generator.save_comic_images([result])
    
    # 示例：生成 6 格漫画
    elif "--comic" in sys.argv:
        scenes = [
            "小沄第一次去钓鱼，对一切都很好奇，站在岸边张望",
            "小沄开始学习如何抛竿，动作还不太熟练",
            "小沄发现了调漂的重要性，恍然大悟",
            "小沄按照学到的方法实践，认真调漂",
            "小沄遇到了一点困难，有点沮丧",
            "小沄终于成功了，钓到了第一条鱼，非常开心"
        ]
        
        results = generator.generate_6panel_comic(scenes)
        print("\n6 格漫画生成完成！")
        
        # 保存所有图片
        generator.save_comic_images(results)
    
    else:
        print("使用方法：")
        print("  python nano_banana_client.py --single    # 生成单格漫画")
        print("  python nano_banana_client.py --comic     # 生成 6 格漫画")
        print("  python nano_banana_client.py --overseas  # 使用海外 Host")
        print("\n环境变量：")
        print("  设置 NANO_BANANA_API_KEY 环境变量来配置 API 密钥")


if __name__ == "__main__":
    main()

