# Supabase 部署指南

## 1. 创建 Supabase 项目

### 步骤 1：访问 Supabase 官网
访问 [Supabase 官网](https://supabase.com/) 并注册/登录账号。

### 步骤 2：创建新项目
1. 登录后，点击右上角的 "New Project" 按钮
2. 填写项目基本信息：
   - 项目名称：输入你的项目名称（如 "gemini-image-generator"）
   - 密码：设置数据库密码（请妥善保管）
   - 选择地区：选择离你目标用户最近的地区
   - 数据库类型：选择 "PostgreSQL"
3. 点击 "Create Project" 按钮

### 步骤 3：等待项目初始化
项目创建后，需要等待几分钟时间进行初始化。初始化完成后，你将进入项目仪表盘。

## 2. 配置数据库表结构

### 步骤 1：创建 `generation_history` 表
1. 在左侧导航栏中，点击 "Database" → "Tables"
2. 点击 "New Table" 按钮
3. 在 "Name" 字段中输入 `generation_history`
4. 勾选 "Enable Row Level Security (RLS)" 选项
5. 点击 "Save" 按钮创建表

### 步骤 2：添加表列
创建表后，点击 "Add column" 按钮添加以下列：

| 列名 | 数据类型 | 约束 | 说明 |
|------|----------|------|------|
| `prompt` | `text` | `not null` | 生成图片的提示词 |
| `aspect_ratio` | `text` | `not null` | 图片宽高比 |
| `image_size` | `text` | `not null` | 图片尺寸 |
| `images` | `jsonb` | `not null` | 生成的图片 URL 数组 |
| `texts` | `jsonb` | `not null` | 生成的文本内容数组 |
| `duration` | `numeric` | `not null` | 生成耗时（秒） |

### 步骤 3：配置 RLS 策略
1. 点击 `generation_history` 表的 "Policies" 标签页
2. 点击 "New Policy" 按钮
3. 选择 "For full access"
4. 输入策略名称（如 "Allow all access"）
5. 点击 "Review" → "Save Policy" 按钮

## 3. 配置环境变量

### 步骤 1：获取 Supabase 凭证
1. 在左侧导航栏中，点击 "Project Settings" → "API"
2. 复制以下凭证：
   - `Project URL`：用于配置 `SUPABASE_URL` 环境变量
   - `Anon Public Key`：用于配置 `SUPABASE_ANON_KEY` 环境变量

### 步骤 2：创建 `.env` 文件
1. 在项目根目录创建 `.env` 文件（如果已存在则编辑）
2. 添加以下内容：

```
# Supabase 配置
SUPABASE_URL=你的 Project URL
SUPABASE_ANON_KEY=你的 Anon Public Key

# Flask 配置（可选）
FLASK_ENV=production
SECRET_KEY=生成一个随机字符串作为密钥
```

## 4. 选择部署平台

### 可选平台

#### 1. **Vercel**
- 适合静态网站和 Serverless 函数
- 支持 Python 应用部署
- 提供免费额度

#### 2. **Render**
- 专门支持 Flask 等 Python 应用
- 提供免费额度
- 部署流程简单

#### 3. **Heroku**
- 传统 PaaS 平台
- 支持 Python 应用
- 免费额度有限

#### 4. **DigitalOcean App Platform**
- 支持多种应用类型
- 提供免费额度
- 界面友好

### 推荐选择：Render

Render 对 Flask 应用的支持较好，部署流程简单，适合小型应用。以下是使用 Render 部署的步骤：

## 5. 使用 Render 部署 Flask 应用

### 步骤 1：准备部署文件

#### 创建 `requirements.txt`（如果已存在则检查）
确保 `requirements.txt` 包含所有必要的依赖：

```
flask>=2.0.0
requests>=2.25.0
supabase>=2.0.0
python-dotenv>=1.0.0
```

#### 创建 `render.yaml`（可选，用于自动部署）
在项目根目录创建 `render.yaml` 文件：

```yaml
services:
  - type: web
    name: gemini-image-generator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

#### 创建 `Procfile`（用于 Heroku 或 Render 部署）
在项目根目录创建 `Procfile` 文件：

```
web: gunicorn app:app
```

### 步骤 2：部署到 Render

1. 访问 [Render 官网](https://render.com/) 并注册/登录
2. 点击 "New" → "Web Service"
3. 选择 "GitHub" 作为代码源，连接你的 GitHub 仓库
4. 配置部署选项：
   - **Name**：输入应用名称
   - **Region**：选择离你目标用户最近的地区
   - **Branch**：选择要部署的分支（如 `main`）
   - **Root Directory**：留空（默认为根目录）
   - **Environment**：选择 "Python"
   - **Build Command**：`pip install -r requirements.txt`
   - **Start Command**：`gunicorn app:app`
5. 点击 "Advanced" 按钮，添加环境变量：
   - `SUPABASE_URL`：你的 Supabase Project URL
   - `SUPABASE_ANON_KEY`：你的 Supabase Anon Public Key
   - `SECRET_KEY`：生成一个随机字符串
6. 点击 "Create Web Service" 按钮

### 步骤 3：等待部署完成

部署过程需要几分钟时间，完成后你将获得一个公共 URL，可以通过该 URL 访问你的应用。

## 6. 测试部署后的应用

### 步骤 1：访问应用 URL
在浏览器中访问 Render 提供的公共 URL，确认应用正常运行。

### 步骤 2：测试核心功能
1. 输入提示词，点击生成按钮
2. 确认图片生成正常
3. 检查历史记录是否保存到 Supabase

### 步骤 3：验证数据库连接
1. 在 Supabase 仪表盘中，点击 "Database" → "Tables"
2. 查看 `generation_history` 表，确认有新的记录生成

## 7. 配置自定义域名（可选）

### 步骤 1：在 Render 中配置自定义域名
1. 在 Render 控制台中，点击你的应用
2. 点击 "Settings" → "Custom Domains"
3. 输入你的域名（如 `app.example.com`）
4. 点击 "Add Custom Domain" 按钮
5. 复制 Render 提供的 CNAME 记录

### 步骤 2：在 DNS 提供商处配置
1. 登录你的 DNS 提供商控制台
2. 添加 CNAME 记录，将你的域名指向 Render 提供的目标地址
3. 等待 DNS 记录生效（通常需要几分钟到几小时）
4. Render 会自动为你的域名配置 SSL 证书

## 8. 监控和维护

### 监控应用
1. 在 Render 控制台中，查看应用的日志和性能指标
2. 在 Supabase 仪表盘中，监控数据库性能和使用情况

### 更新应用
1. 将代码推送到 GitHub 仓库
2. Render 会自动检测到代码变更并重新部署
3. 等待部署完成后测试应用

## 9. 常见问题和解决方案

### 问题 1：应用无法连接到 Supabase
**解决方案**：
- 检查 `.env` 文件中的 `SUPABASE_URL` 和 `SUPABASE_ANON_KEY` 是否正确
- 确认 Supabase 项目的 RLS 策略是否配置正确
- 检查网络连接是否正常

### 问题 2：图片生成失败
**解决方案**：
- 检查 API 密钥是否正确
- 查看应用日志，确认错误信息
- 检查生成配置是否正确

### 问题 3：历史记录无法保存
**解决方案**：
- 确认 `generation_history` 表已正确创建
- 检查 RLS 策略是否允许插入操作
- 查看应用日志，确认错误信息

## 10. 优化建议

1. **使用生产级 WSGI 服务器**：使用 Gunicorn 或 uWSGI 替代 Flask 内置服务器
2. **配置 CDN**：为静态资源配置 CDN，提高访问速度
3. **启用缓存**：对频繁访问的数据启用缓存
4. **定期备份**：定期备份 Supabase 数据库
5. **监控性能**：设置性能监控，及时发现和解决问题

## 11. 成本优化

1. **选择合适的部署平台**：根据应用规模选择合适的部署平台和计划
2. **优化资源使用**：根据应用负载调整服务器配置
3. **清理旧数据**：定期清理不再需要的历史记录
4. **使用免费额度**：充分利用各平台的免费额度

---

通过以上步骤，你可以成功将 Gemini 图片生成 Web 应用部署到 Supabase 和 Render 平台。如果遇到任何问题，请查看相关平台的文档或寻求社区支持。