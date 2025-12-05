FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p uploads static/outputs && chmod 777 uploads static/outputs

# Hugging Face Spaces 默认使用 7860 端口
EXPOSE 7860

# 启动命令
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
