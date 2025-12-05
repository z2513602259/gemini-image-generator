-- Supabase 数据库设置脚本
-- 在 Supabase Dashboard -> SQL Editor 中运行此脚本

-- 创建 generation_history 表
CREATE TABLE IF NOT EXISTS generation_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    prompt TEXT NOT NULL,
    aspect_ratio TEXT NOT NULL,
    image_size TEXT NOT NULL,
    images JSONB NOT NULL DEFAULT '[]',
    texts JSONB NOT NULL DEFAULT '[]',
    duration NUMERIC NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 启用 Row Level Security
ALTER TABLE generation_history ENABLE ROW LEVEL SECURITY;

-- 创建允许所有操作的策略（公开访问）
-- 注意：生产环境建议配置更严格的策略
CREATE POLICY "Allow all access" ON generation_history
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- 创建索引以优化查询性能
CREATE INDEX IF NOT EXISTS idx_generation_history_created_at 
    ON generation_history(created_at DESC);

-- 验证表结构
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'generation_history';
