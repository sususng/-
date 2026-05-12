# 课堂模拟CrewAI

基于 CrewAI 框架的高中信息技术课堂模拟系统，支持AI备课和课堂模拟。

## 📋 项目简介

**课堂模拟CrewAI** 是一个智能教学辅助系统，通过AI技术模拟真实的课堂教学场景，帮助教师：

- 🤖 **AI备课** - 自动生成教案、PPT脚本、说课稿、课堂时间线等教学文件
- 🎭 **课堂模拟** - 模拟40分钟课堂教学，包含教师主导策略和学生行为模拟
- 👥 **多角色审核** - 听课教师、教导主任、内容审核官多维度审核
- 👨‍🎓 **学生反馈模拟** - 学优生、中等生、后进生三类学生的反馈模拟

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 备课流程 | 协同备课 + 双重审核（教导主任 + 内容审核官） |
| 课堂模拟 | 40分钟完整模拟 + 三重审核 |
| 7个Agent角色 | 主教师、听课教师、教导主任、内容审核官、三类学生 |
| 双重审核机制 | 教学专业审核 + 内容合规性审核 |

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| AI框架 | CrewAI 1.14.4 |
| 语言模型 | MiniMax-M2.7 / OpenAI GPT系列 |
| 运行环境 | Python 3.10-3.13 |
| 容器化 | Docker + Docker Compose |
| 项目管理 | uv / pip |

## 🚀 快速开始

### 方法一：Windows本地部署（推荐新手）

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd classroom_simulation

# 2. 运行部署脚本
deploy.bat

# 3. 配置API密钥
# 编辑 .env 文件，填入您的 API 密钥

# 4. 测试运行
python -m classroom_simulation.main --test-tools
```

### 方法二：Docker部署（推荐开发者）

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd classroom_simulation

# 2. 配置API密钥
copy .env.example .env
# 编辑 .env 文件，填入您的 API 密钥

# 3. 构建并启动
docker-compose up -d

# 4. 测试运行
docker-compose exec classroom_simulation python -m classroom_simulation.main --test-tools
```

## 📖 使用方法

### 1. 配置API密钥

复制 `.env.example` 为 `.env`，填入您的MiniMax或OpenAI API密钥：

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.minimaxi.com/v1
MODEL=MiniMax-M2.7
```

### 2. 运行备课流程

```bash
# 基本备课
python -m classroom_simulation.main --topic "数据采集与编码" --mode prep

# 指定输出目录
python -m classroom_simulation.main --topic "Python数据分析" --mode prep -o output/Python数据分析
```

### 3. 运行课堂模拟

```bash
# 基于备课包进行课堂模拟
python -m classroom_simulation.main --mode demo --prep-package "output/数据采集与编码"
```

### 4. Docker环境使用

```bash
# 备课
docker-compose exec classroom_simulation python -m classroom_simulation.main --topic "数据采集与编码" --mode prep

# 课堂模拟
docker-compose exec classroom_simulation python -m classroom_simulation.main --mode demo --prep-package "output/数据采集与编码"

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec classroom_simulation bash
```

## 📁 项目结构

```
classroom_simulation/
├── src/
│   └── classroom_simulation/
│       ├── main.py                 # 程序入口
│       ├── crew.py                 # 基础Crew类
│       ├── agents/                 # Agent定义
│       │   ├── leader_teacher.py   # 主讲教师
│       │   ├── peer_teacher.py     # 听课教师
│       │   ├── student_agents.py   # 学生Agent
│       │   ├── academic_director.py # 教导主任
│       │   └── content_auditor.py  # 内容审核官
│       ├── crews/                  # Crew流程
│       │   ├── lesson_prep_crew/   # 备课流程
│       │   └── class_demo_crew/    # 课堂模拟流程
│       ├── tools/                  # 工具集
│       │   ├── file_tools.py       # 文件操作
│       │   ├── search_tools.py     # 搜索工具
│       │   └── doc_converter.py    # 文档转换
│       └── utils/                  # 工具模块
├── tests/                          # 测试目录
├── knowledge/                       # 知识库（可添加教学案例）
│   └── agent/
├── output/                         # 输出目录（运行时生成）
├── Dockerfile                      # Docker镜像配置
├── docker-compose.yml             # Docker服务编排
├── deploy.bat                     # Windows部署脚本
├── DOCKER_GUIDE.md                # Docker使用指南
├── AGENTS.md                      # CrewAI参考文档
├── pyproject.toml                 # 项目配置
└── pytest.ini                     # pytest配置
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `OPENAI_API_KEY` | LLM API密钥 | ✅ |
| `OPENAI_API_BASE` | API地址（MiniMax用） | ✅ |
| `MODEL` | 模型名称 | ✅ |
| `CREWAI_MEMORY_ENABLED` | 是否启用记忆 | ❌ |

### Agent配置

系统包含7个Agent，配置在 `src/classroom_simulation/crews/*/config/` 目录：

- **主教师** (temperature=0.7) - 备课和授课
- **听课教师** (temperature=0.8) - 协同备课和观察
- **教导主任** (temperature=0.5) - 教学审核
- **内容审核官** (temperature=0.3) - 合规性审核
- **学优生** (temperature=0.9) - 学优生模拟
- **中等生** (temperature=0.7) - 中等生模拟
- **后进生** (temperature=0.9) - 后进生模拟

## 📚 文档

- [Docker部署指南](DOCKER_GUIDE.md) - 详细的Docker部署说明
- [AGENTS.md](AGENTS.md) - CrewAI官方参考文档

## ⚠️ 注意事项

1. **API密钥安全**：不要将 `.env` 文件提交到GitHub，已通过 `.gitignore` 排除
2. **首次运行**：首次运行会下载模型，可能需要几分钟
3. **网络要求**：需要能够访问API服务（MiniMax或OpenAI）
4. **输出文件**：运行产生的文件保存在 `output/` 目录

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [CrewAI](https://github.com/crewAIInc/crewAI) - AI Agent框架
- [MiniMax](https://www.minimaxi.com/) - 大语言模型服务
