# Docker部署指南

## 目录

- [快速开始](#快速开始)
- [方案一：Windows本地部署](#方案一windows本地部署)
- [方案二：Docker容器部署](#方案二docker容器部署)
- [常见问题](#常见问题)

---

## 快速开始

### 换电脑后的部署流程

#### 方案一：Windows本地部署（推荐新手）

```bash
# 1. 克隆项目
git clone <your-repo-url> classroom_simulation
cd classroom_simulation

# 2. 运行部署脚本
deploy.bat

# 3. 编辑.env文件填入API密钥
notepad .env

# 4. 开始使用
python -m classroom_simulation.main --test-tools
```

#### 方案二：Docker容器部署（推荐开发者）

```bash
# 1. 克隆项目
git clone <your-repo-url> classroom_simulation
cd classroom_simulation

# 2. 配置.env文件
copy .env.example .env
notepad .env  # 填入API密钥

# 3. 构建并启动容器
docker-compose up -d

# 4. 查看运行状态
docker-compose ps

# 5. 进入容器执行命令
docker-compose exec classroom_simulation python -m classroom_simulation.main --test-tools
```

---

## 方案一：Windows本地部署

### 前置要求

- Windows 10/11
- Python 3.10-3.13（[下载地址](https://www.python.org/downloads/)）
- Git（[下载地址](https://git-scm.com/download/win)）

### 详细步骤

1. **安装Python**
   - 下载Python 3.11或更高版本
   - 安装时勾选"Add Python to PATH"
   - 验证安装：`python --version`

2. **克隆项目**
   ```bash
   git clone <your-repo-url> classroom_simulation
   cd classroom_simulation
   ```

3. **运行部署脚本**
   ```bash
   deploy.bat
   ```
   脚本会自动：
   - 创建虚拟环境（.venv）
   - 安装所有依赖
   - 创建.env配置文件模板

4. **配置API密钥**
   编辑 `.env` 文件：
   ```env
   OPENAI_API_KEY=your-actual-api-key
   OPENAI_API_BASE=https://api.minimaxi.com/v1
   ```

5. **开始使用**
   ```bash
   # 测试工具
   python -m classroom_simulation.main --test-tools

   # 备课
   python -m classroom_simulation.main --topic "数据采集与编码" --mode prep

   # 课堂模拟
   python -m classroom_simulation.main --mode demo --prep-package "output\数据采集与编码"
   ```

---

## 方案二：Docker容器部署

### 前置要求

- Windows 10/11 Pro或Enterprise
- Docker Desktop（[下载地址](https://www.docker.com/products/docker-desktop)）
- 至少4GB可用内存

### 安装Docker Desktop

1. 下载Docker Desktop for Windows
2. 运行安装程序
3. 启动Docker Desktop（首次启动可能需要几分钟）
4. 验证安装：
   ```bash
   docker --version
   docker-compose --version
   ```

### 构建镜像

```bash
# 进入项目目录
cd classroom_simulation

# 构建镜像（首次需要几分钟）
docker build -t classroom_simulation:latest .

# 查看镜像
docker images
```

### 使用Docker Compose运行

1. **创建.env文件**
   ```bash
   copy .env.example .env
   notepad .env
   ```

2. **启动服务**
   ```bash
   # 前台运行（查看日志）
   docker-compose up

   # 后台运行
   docker-compose up -d

   # 查看状态
   docker-compose ps
   ```

3. **查看日志**
   ```bash
   # 实时日志
   docker-compose logs -f

   # 查看最近日志
   docker-compose logs --tail=100
   ```

4. **执行命令**
   ```bash
   # 测试工具
   docker-compose exec classroom_simulation python -m classroom_simulation.main --test-tools

   # 备课
   docker-compose exec classroom_simulation python -m classroom_simulation.main --topic "数据采集与编码" --mode prep

   # 进入容器Shell
   docker-compose exec classroom_simulation bash
   ```

5. **停止服务**
   ```bash
   docker-compose down

   # 同时删除数据卷
   docker-compose down -v
   ```

### 调试模式（Jupyter Notebook）

启动Jupyter Notebook用于调试：

```bash
# 启动包含Jupyter的服务
docker-compose --profile debug up -d

# 访问 http://localhost:8888
# Token: classroom2024
```

---

## 常见问题

### Q: Docker Desktop启动失败

**A:** 确保：
1. WSL 2已启用（Windows功能 → 勾选"适用于Linux的Windows子系统"）
2. 虚拟化已启用（BIOS设置）
3. 至少有4GB内存分配给Docker

### Q: 容器内无法访问网络

**A:** 检查Docker网络：
```bash
docker network ls
docker network inspect classroom_simulation_classroom_network
```

### Q: 端口8888被占用

**A:** 修改docker-compose.yml中的端口映射：
```yaml
ports:
  - "8889:8888"  # 改为8889
```

### Q: 构建镜像太慢

**A:** 使用国内镜像加速。在Docker Desktop设置 → Docker Engine中添加：
```json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
```

### Q: 换电脑后数据丢失

**A:** 确保挂载了卷：
- `./output:/app/output` - 备课结果
- `./knowledge:/app/knowledge` - 知识库
- `./.env:/app/.env:ro` - 配置（只读）

### Q: 如何更新到最新版本

**本地部署：**
```bash
git pull
deploy.bat
```

**Docker部署：**
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `Dockerfile` | Docker镜像构建配置 |
| `docker-compose.yml` | Docker服务编排配置 |
| `.dockerignore` | Docker构建排除文件 |
| `deploy.bat` | Windows本地部署脚本 |

---

## 卸载清理

**本地部署：**
```bash
# 删除虚拟环境
rmdir /s /q .venv

# 删除输出目录（可选）
rmdir /s /q output
```

**Docker部署：**
```bash
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi classroom_simulation:latest

# 完全清理
docker system prune -a
```
