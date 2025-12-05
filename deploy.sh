#!/bin/bash

# Gemini 图片生成器部署脚本
# 用于将应用部署到 Supabase

echo "=== Gemini 图片生成器部署脚本 ==="
echo ""

# 检查是否安装了 Supabase CLI
if ! command -v supabase &> /dev/null; then
    echo "❌ 未安装 Supabase CLI，请先安装："
    echo "   npm install -g supabase"
    exit 1
fi

echo "✅ Supabase CLI 已安装"
echo ""

# 检查是否登录了 Supabase
if ! supabase whoami &> /dev/null; then
    echo "🔐 请登录 Supabase："
    supabase login
    echo ""
fi

echo "✅ 已登录 Supabase"
echo ""

# 提示用户输入项目信息
echo "📝 请输入 Supabase 项目信息："
read -p "项目引用 (project-ref) [格式：abc123xyz]：" PROJECT_REF
read -p "Supabase URL [格式：https://abc123xyz.supabase.co]：" SUPABASE_URL
read -p "Supabase Anon Key：" SUPABASE_ANON_KEY

echo ""
echo "📋 项目信息："
echo "   Project Ref: $PROJECT_REF"
echo "   Supabase URL: $SUPABASE_URL"
echo "   Supabase Anon Key: $SUPABASE_ANON_KEY"
echo ""

# 创建 .env 文件
echo "📁 创建 .env 文件..."
cat > .env << EOF
# Supabase 配置
SUPABASE_URL=$SUPABASE_URL
SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY

# 应用配置
FLASK_ENV=production
FLASK_APP=app.py
EOF

echo "✅ .env 文件已创建"
echo ""

# 创建 Supabase 配置文件
echo "📁 创建 Supabase 配置文件..."
if [ ! -d ".supabase" ]; then
    mkdir -p .supabase
fi

cat > .supabase/config.toml << EOF
[project]
projectRef = "$PROJECT_REF"
EOF

echo "✅ Supabase 配置文件已创建"
echo ""

# 链接到 Supabase 项目
echo "🔗 链接到 Supabase 项目..."
supabase link --project-ref $PROJECT_REF

echo "✅ 已链接到 Supabase 项目"
echo ""

# 创建历史记录表
echo "🗄️ 创建历史记录表..."
supabase sql -f - << EOF
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
EOF

echo "✅ 历史记录表已创建"
echo ""

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

echo "✅ 依赖安装完成"
echo ""

# 提示用户部署后端应用
echo "🚀 现在您可以部署后端应用了！"
echo ""
echo "📋 部署选项："
echo "1. 使用 Vercel 部署：https://vercel.com/"
echo "2. 使用 Render 部署：https://render.com/"
echo "3. 使用 Railway 部署：https://railway.app/"
echo "4. 使用 Docker 容器化部署"
echo ""
echo "📝 部署注意事项："
echo "- 确保将 .env 文件中的环境变量添加到部署平台"
echo "- 确保部署平台支持 Python 3.7+"
echo "- 确保设置了正确的 PORT 环境变量（默认为 5000）"
echo ""
echo "🎉 部署准备工作已完成！"
echo ""