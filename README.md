# Gemini 图片生成器

一个基于 Gemini AI 的图片生成 Web 应用，支持文本提示词生成图片、上传参考图片和历史记录功能。

## 功能特性

- ✨ 文本提示词生成图片
- 📷 支持上传参考图片
- 📱 响应式设计，适配移动端和桌面端
- 📚 历史记录功能（保存在浏览器本地存储）
- ⚙️ 可配置 API Key 和 API URL
- 🎨 支持多种图片比例和分辨率

## 技术栈

- **后端**: Python Flask
- **前端**: HTML, CSS, JavaScript (使用 Tailwind CSS 和 Font Awesome)
- **AI 模型**: Gemini 3 Pro Image Preview

## 本地运行

### 环境要求

- Python 3.7 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆或下载项目到本地

2. 安装依赖包
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用
   ```bash
   python app.py
   ```

4. 在浏览器中访问 `http://localhost:5000`

## Supabase 部署方案

### 方案一：使用 Supabase 作为数据库（推荐）

将历史记录从浏览器本地存储迁移到 Supabase 数据库，实现跨设备同步和持久化存储。

#### 步骤

1. **创建 Supabase 项目**
   - 访问 [Supabase](https://supabase.com/) 并注册账号
   - 创建一个新的 Supabase 项目

2. **创建历史记录表**
   - 在 Supabase 控制台中，进入 "SQL Editor"
   - 运行以下 SQL 脚本创建历史记录表：
     ```sql
     CREATE TABLE IF NOT EXISTS generation_history (
       id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
       prompt TEXT NOT NULL,
       aspect_ratio TEXT NOT NULL,
       image_size TEXT NOT NULL,
       images JSONB NOT NULL,
       texts JSONB NOT NULL,
       duration FLOAT NOT NULL,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
     );
     ```

3. **安装 Supabase Python 客户端**
   ```bash
   pip install supabase
   ```

4. **修改后端代码集成 Supabase**
   - 在 `app.py` 中添加 Supabase 配置和初始化
   - 修改历史记录相关的 API 端点
   - 将历史记录保存到 Supabase 数据库

5. **部署后端应用**
   - 可以部署到 Vercel、Render、Railway 等支持 Python 的平台
   - 或使用 Docker 容器化部署

6. **部署前端静态文件**（可选）
   - 可以将静态文件托管在 Supabase Hosting
   - 或继续使用后端服务器托管

### 方案二：仅使用 Supabase Hosting 托管静态文件

如果不需要数据库功能，可以仅使用 Supabase Hosting 托管前端静态文件，后端仍部署在其他平台。

#### 步骤

1. **构建前端静态文件**
   - 目前项目是前后端一体的 Flask 应用，需要将前端分离
   - 可以使用 Vite 或 Webpack 构建前端

2. **部署到 Supabase Hosting**
   - 在项目根目录创建 `public` 文件夹，将构建好的静态文件放入其中
   - 安装 Supabase CLI：
     ```bash
     npm install -g supabase
     ```
   - 登录 Supabase：
     ```bash
     supabase login
     ```
   - 初始化 Supabase 项目：
     ```bash
     supabase init
     ```
   - 链接到现有 Supabase 项目：
     ```bash
     supabase link --project-ref <your-project-ref>
     ```
   - 部署静态文件：
     ```bash
     supabase deploy
     ```

### 方案三：使用 Supabase Edge Functions 重写后端

将 Flask 后端重写为 Supabase Edge Functions（使用 TypeScript/JavaScript）。

#### 步骤

1. **创建 Supabase Edge Functions**
   - 安装 Supabase CLI
   - 创建新的 Edge Function：
     ```bash
     supabase functions new generate-image
     ```

2. **重写后端逻辑**
   - 使用 TypeScript/JavaScript 重写生成图片的逻辑
   - 配置 API 路由

3. **部署 Edge Functions**
   ```bash
   supabase functions deploy generate-image
   ```

4. **部署前端静态文件**
   - 参考方案二中的步骤

## 环境变量配置

如果使用 Supabase 数据库，需要配置以下环境变量：

- `SUPABASE_URL`: Supabase 项目 URL
- `SUPABASE_ANON_KEY`: Supabase 匿名访问密钥

## 项目结构

```
gemini3pro/
├── app.py                  # Flask 应用主文件
├── config.json             # 配置文件
├── requirements.txt        # 依赖包列表
├── static/                 # 静态资源文件夹
│   └── outputs/            # 生成的图片存储目录
├── templates/              # HTML 模板文件夹
│   └── index.html          # 主页面模板
└── uploads/                # 上传文件临时存储目录
```

## API 端点

### GET /
返回主页面

### GET /settings
获取当前设置（API Key 和 API URL）

### POST /settings
更新设置

### POST /generate
生成图片
- **请求参数**：
  - `prompt`: 提示词（必填）
  - `aspect_ratio`: 图片比例（可选，默认 1:1）
  - `image_size`: 图片分辨率（可选，默认 2K）
  - `images`: 参考图片（可选，支持多个）

- **响应格式**：
  ```json
  {
    "success": true,
    "results": [
      {
        "type": "image",
        "url": "/static/outputs/filename.png"
      },
      {
        "type": "text",
        "content": "生成的文本内容"
      }
    ]
  }
  ```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
