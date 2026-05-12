# 课堂模拟CrewAI Docker镜像
# 基于Python 3.11 slim版本构建

FROM python:3.11-slim

LABEL maintainer="Classroom Simulation Team"
LABEL description="课堂模拟CrewAI - 基于CrewAI框架的课堂教学模拟系统"
LABEL version="1.0.0"

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PROJECT_NAME=classroom_simulation

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 设置工作目录
WORKDIR /app

# 复制依赖配置文件
COPY pyproject.toml* ./
COPY uv.lock* ./

# 安装Python依赖
# 使用pip安装以便更好的兼容性
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p output knowledge/agent && \
    chown -R python:python /app

# 切换到非root用户
USER python

# 暴露端口（用于Jupyter等工具）
EXPOSE 8888

# 默认命令 - 显示帮助信息
CMD ["python", "-m", "classroom_simulation.main", "--help"]
