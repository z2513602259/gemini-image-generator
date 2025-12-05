"""
Gemini 图片生成 Web 应用
"""
import os
import json
import base64
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from supabase import create_client, Client

# 加载环境变量
load_dotenv()

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# 初始化 Supabase 客户端
if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
else:
    supabase = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'
app.config['CONFIG_FILE'] = 'config.json'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 默认配置
DEFAULT_CONFIG = {
    "api_key": "sk-eQarxTOr5XGyXKzAfIIDMImKDxy6WrLLqUgGzIjlH67LGZKV",
    "api_url": "https://api.vectorengine.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"
}

def load_config():
    """加载配置"""
    if os.path.exists(app.config['CONFIG_FILE']):
        try:
            with open(app.config['CONFIG_FILE'], 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(app.config['CONFIG_FILE'], 'w') as f:
        json.dump(config, f, indent=2)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET'])
def get_settings():
    """获取当前设置"""
    config = load_config()
    # 隐藏部分 API Key
    masked_key = config['api_key']
    if len(masked_key) > 8:
        masked_key = masked_key[:4] + '*' * (len(masked_key) - 8) + masked_key[-4:]
    return jsonify({
        'api_key': config['api_key'],
        'api_key_masked': masked_key,
        'api_url': config['api_url']
    })

@app.route('/settings', methods=['POST'])
def update_settings():
    """更新设置"""
    try:
        data = request.get_json()
        config = load_config()
        
        if 'api_key' in data and data['api_key']:
            config['api_key'] = data['api_key']
        if 'api_url' in data and data['api_url']:
            config['api_url'] = data['api_url']
        
        save_config(config)
        return jsonify({'success': True, 'message': '设置已保存'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 记录生成开始时间
        start_time = datetime.now()
        
        # 加载配置
        config = load_config()
        api_key = config['api_key']
        api_url = config['api_url']
        
        # 获取提示词
        prompt = request.form.get('prompt', '')
        if not prompt:
            return jsonify({'error': '请输入提示词'}), 400
        
        # 获取配置
        aspect_ratio = request.form.get('aspect_ratio', '1:1')
        image_size = request.form.get('image_size', '2K')
        
        # 构建请求parts
        parts = [{"text": prompt}]
        
        # 处理上传的图片
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                image_data = base64.b64encode(file.read()).decode('utf-8')
                mime_type = f"image/{file.filename.rsplit('.', 1)[1].lower()}"
                if mime_type == 'image/jpg':
                    mime_type = 'image/jpeg'
                parts.append({
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": image_data
                    }
                })
        
        # 发送API请求
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
                        "aspectRatio": aspect_ratio,
                        "imageSize": image_size
                    }
                }
            },
            proxies={"http": None, "https": None},
            timeout=300
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'API请求失败: {response.status_code}', 'details': response.text}), 500
        
        data = response.json()
        results = []
        
        # 处理返回结果
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "text" in part:
                    results.append({'type': 'text', 'content': part['text']})
                if "inlineData" in part:
                    # 直接返回 Base64 数据
                    img_b64 = part["inlineData"]["data"]
                    mime_type = part["inlineData"]["mimeType"] if "mimeType" in part["inlineData"] else "image/png"
                    data_url = f"data:{mime_type};base64,{img_b64}"
                    results.append({'type': 'image', 'url': data_url})
        
        if not results:
            return jsonify({'error': '未生成任何内容'}), 500
            
        # 保存历史记录到 Supabase
        if supabase:
            try:
                # 注意：Base64 数据太长，不适合直接存数据库。
                # 这里我们只存一个标记，或者如果不上传到 Storage，就不存 url 字段
                # 改进方案：如果需要历史记录看图，必须集成 Supabase Storage
                # 临时方案：存一个占位符，或者如果 Supabase 支持大文本可以存（但不推荐）
                
                # Vercel 版暂时不存 Base64 到数据库，防止请求过大失败
                # images = [item['url'] for item in results if item['type'] == 'image']
                images = ["(图片未保存到云端)"] * len([x for x in results if x['type'] == 'image'])
                
                texts = [item['content'] for item in results if item['type'] == 'text']
                
                # 计算生成耗时
                duration = (datetime.now() - start_time).total_seconds()
                
                supabase.table('generation_history').insert({
                    'prompt': prompt,
                    'aspect_ratio': aspect_ratio,
                    'image_size': image_size,
                    'images': images,
                    'texts': texts,
                    'duration': duration
                }).execute()
            except Exception as e:
                print(f"保存历史记录到 Supabase 失败: {e}")
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 历史记录相关 API
@app.route('/history', methods=['GET'])
def get_history():
    """获取历史记录"""
    if not supabase:
        return jsonify({'error': 'Supabase 未配置'}), 500
    
    try:
        response = supabase.table('generation_history')\
            .select('*')\
            .order('created_at', desc=True)\
            .execute()
        
        history = response.data
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['DELETE'])
def clear_history():
    """清空历史记录"""
    if not supabase:
        return jsonify({'error': 'Supabase 未配置'}), 500
    
    try:
        supabase.table('generation_history').delete().execute()
        return jsonify({'success': True, 'message': '历史记录已清空'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
