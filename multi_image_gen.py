# 多图参考示例（Python）
# 功能：使用Gemini 3 Pro模型，根据参考图片生成新的室内设计渲染图

# 导入所需模块
import requests
import base64
import json
import os
from datetime import datetime


def load_images(image_paths):
    """
    加载图片并转换为base64格式
    
    Args:
        image_paths (list): 图片文件路径列表
        
    Returns:
        list: 包含图片base64数据的字典列表
    """
    images_data = []
    for path in image_paths:
        try:
            # 读取图片文件并转换为base64格式
            with open(path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            
            # 添加到图片数据列表
            images_data.append({
                "inline_data": {
                    "mime_type": "image/png",  # 假设所有图片都是PNG格式
                    "data": image_data
                }
            })
            print(f"成功加载图片: {path}")
        except Exception as e:
            print(f"加载图片失败 {path}: {e}")
    return images_data


def send_request(api_key, api_url, prompt, images_data):
    """
    发送API请求生成图片
    
    Args:
        api_key (str): API密钥
        api_url (str): API请求URL
        prompt (str): 生成图片的文本提示
        images_data (list): 包含图片base64数据的字典列表
        
    Returns:
        dict: API响应数据
    """
    # 构建请求内容
    parts = [{"text": prompt}]
    parts.extend(images_data)
    
    try:
        print("正在发送请求...")
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "contents": [{"parts": parts}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageConfig": {
                        "aspectRatio": "1:1",  # 图片比例 1:1
                        "imageSize": "2K"  # 图片分辨率 2K
                    }
                }
            },
            proxies={"http": None, "https": None},  # 禁用代理
            timeout=300  # 5分钟超时
        )
        
        # 检查响应状态码
        response.raise_for_status()
        print(f"请求成功，状态码: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"处理请求响应失败: {e}")
        return None


def save_images(response_data):
    """
    处理API响应并保存生成的图片
    
    Args:
        response_data (dict): API响应数据
        
    Returns:
        int: 成功保存的图片数量
    """
    saved_count = 0
    
    if not response_data:
        return saved_count
    
    try:
        # 遍历所有候选结果
        for i, candidate in enumerate(response_data.get("candidates", [])):
            print(f"\n候选结果 {i}:")
            
            # 获取候选结果的内容
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            
            # 遍历内容中的所有部分
            for j, part in enumerate(parts):
                print(f"  内容部分 {j} 包含的键: {list(part.keys())}")
                
                # 处理文本内容
                if "text" in part:
                    text = part["text"]
                    print(f"    文本内容: {text[:200]}...")
                
                # 处理图片内容
                if "inlineData" in part:
                    try:
                        # 获取图片数据和MIME类型
                        inline_data = part["inlineData"]
                        mime_type = inline_data.get("mimeType", "image/png")
                        img_data_base64 = inline_data["data"]
                        
                        print(f"    包含图片数据! MIME类型: {mime_type}")
                        
                        # 解码base64图片数据
                        img_data = base64.b64decode(img_data_base64)
                        
                        # 生成文件名（包含时间戳和索引）
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"output_{timestamp}_{i}_{j}.png"
                        
                        # 保存图片文件
                        with open(filename, "wb") as f:
                            f.write(img_data)
                        
                        print(f"    图片已保存到: {filename}")
                        saved_count += 1
                    except Exception as e:
                        print(f"    保存图片失败: {e}")
    except Exception as e:
        print(f"处理响应数据失败: {e}")
    
    return saved_count


def main():
    """
    主函数，整合所有流程
    """
    # 配置参数
    # 建议：从环境变量读取API_KEY，提高安全性
    # API_KEY = os.getenv("API_KEY")
    API_KEY = "sk-eQarxTOr5XGyXKzAfIIDMImKDxy6WrLLqUgGzIjlH67LGZKV"
    API_URL = "https://api.vectorengine.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"
    
    # 生成图片的文本提示
    prompt = "Use the texture from 01.png to generate interior design renderings with a minimalist style, rich content, and a large scene. Avoid stitching together multiple images."
    
    # 参考图片路径列表
    image_paths = ["01.png"]
    
    # 加载图片
    images_data = load_images(image_paths)
    if not images_data:
        print("没有成功加载任何图片，无法继续")
        return
    
    # 发送请求生成图片
    response_data = send_request(API_KEY, API_URL, prompt, images_data)
    if not response_data:
        print("请求失败，无法继续")
        return
    
    # 保存生成的图片
    saved_count = save_images(response_data)
    print(f"\n处理完成，成功保存 {saved_count} 张图片")


if __name__ == "__main__":
    main()
