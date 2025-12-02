# 多图参考示例（Python）
import requests
import base64
from datetime import datetime

API_KEY = "sk-WzpmVCuL7FOcvoMOB322Af46679d445b9fA19cE86dF2C905"
API_URL = "https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 准备多张参考图片
image_paths = ["01.png"]
parts = [{"text": "Use the texture from 01.png to generate interior design renderings with a minimalist style, rich content, and a large scene. Avoid stitching together multiple images."}]

for path in image_paths:
    with open(path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    parts.append({
        "inline_data": {
            "mime_type": "image/png",
            "data": image_data
        }
    })

# 发送请求（禁用代理，设置超时）
print("正在发送请求...")
response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": "1:1",  # 图片比例
                "imageSize": "2K"  # 图片分辨率
            }
        }
    },
    proxies={"http": None, "https": None},  # 禁用代理
    timeout=300  # 5分钟超时
)

print("Status Code:", response.status_code)
import json
data = response.json()

# 检查所有parts
for i, candidate in enumerate(data.get("candidates", [])):
    print(f"Candidate {i}:")
    for j, part in enumerate(candidate.get("content", {}).get("parts", [])):
        print(f"  Part {j} keys: {list(part.keys())}")
        if "text" in part:
            print(f"    Text: {part['text'][:200]}...")
        if "inlineData" in part:
            print(f"    Has inlineData! mime_type: {part['inlineData'].get('mimeType')}")
            img_data = base64.b64decode(part["inlineData"]["data"])
            filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"    Image saved to {filename}")

# 保存生成的图片
if response.status_code == 200:
    data = response.json()
    try:
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inline_data" in part:
                    img_data = base64.b64decode(part["inline_data"]["data"])
                    with open("output.png", "wb") as f:
                        f.write(img_data)
                    print("Image saved to output.png")
    except Exception as e:
        print(f"Error saving image: {e}")
