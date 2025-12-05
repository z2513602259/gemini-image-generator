# API测试脚本
# 功能：测试Gemini API连接是否正常

import requests
import json

# API配置
API_KEY = "sk-eQarxTOr5XGyXKzAfIIDMImKDxy6WrLLqUgGzIjlH67LGZKV"
API_URL = "https://api.vectorengine.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"

def test_api_connection():
    """
    测试API连接是否正常
    """
    print("正在测试API连接...")
    print(f"API URL: {API_URL}")
    print(f"API Key: {API_KEY[:4]}...{API_KEY[-4:]}")
    
    # 构建测试请求
    test_payload = {
        "contents": [{
            "parts": [{
                "text": "Test API connection"
            }]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT"],
            "imageConfig": {
                "aspectRatio": "1:1",
                "imageSize": "2K"
            }
        }
    }
    
    try:
        # 发送请求
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=test_payload,
            proxies={"http": None, "https": None},
            timeout=60
        )
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API连接成功！")
            # 解析响应
            response_data = response.json()
            print("\n响应数据:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            return True
        else:
            print("❌ API连接失败！")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 响应解析失败: {e}")
        print(f"响应内容: {response.text}")
        return False

if __name__ == "__main__":
    test_api_connection()