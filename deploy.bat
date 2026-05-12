@echo off
chcp 65001 >nul
echo ======================================
echo 课堂模拟CrewAI - 快速部署脚本
echo ======================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% == 0 (
    echo [提示] 以管理员权限运行
)

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装Python或未添加到PATH
    echo 请先安装Python 3.10-3.13
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 获取Python版本
python --version > temp_version.txt
set /p PYTHON_VERSION=<temp_version.txt
del temp_version.txt
echo [检查] 检测到 %PYTHON_VERSION%

REM 检查虚拟环境
if exist ".venv" (
    echo [2/5] 虚拟环境已存在，跳过创建...
) else (
    echo [1/5] 创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo [2/5] 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 升级pip
echo [3/5] 升级pip...
python -m pip install --upgrade pip --quiet

REM 安装依赖
echo [4/5] 安装项目依赖...
pip install -e . --quiet
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

REM 配置环境变量
if exist ".env" (
    echo [5/5] 环境配置文件已存在，跳过创建...
) else (
    echo [5/5] 创建环境配置文件模板...
    (
        echo # ============================================================
        echo # 课堂模拟系统环境配置
        echo # ============================================================
        echo.
        echo # LLM配置 - MiniMax 2.7 ^(OpenAI兼容格式^)
        echo OPENAI_API_KEY=your-api-key-here
        echo OPENAI_API_BASE=https://api.minimaxi.com/v1
        echo.
        echo # 模型配置
        echo MODEL=MiniMax-M2.7
        echo OPENAI_MODEL_NAME=MiniMax-M2.7
        echo.
        echo # CrewAI配置
        echo CREWAI_MEMORY_ENABLED=false
        echo.
        echo # 项目配置
        echo PROJECT_NAME=课堂模拟CrewAIv2
        echo DEFAULT_TOPIC=数据采集与编码
        echo LESSON_DURATION=40
        echo.
        echo # 路径配置
        echo PREP_PACKAGE_DIR=output
        echo KNOWLEDGE_BASE_DIR=knowledge
    ) > .env
    echo [注意] 已创建 .env 配置文件模板
    echo [注意] 请编辑 .env 文件，填入您的API密钥
)

REM 创建必要目录
if not exist "output" mkdir output
if not exist "knowledge\agent" mkdir knowledge\agent 2>nul

echo.
echo ======================================
echo 部署完成！
echo ======================================
echo.
echo 快速运行命令：
echo.
echo 测试工具:
echo   python -m classroom_simulation.main --test-tools
echo.
echo 备课流程:
echo   python -m classroom_simulation.main --topic "数据采集与编码" --mode prep
echo.
echo 课堂模拟:
echo   python -m classroom_simulation.main --mode demo --prep-package "output\数据采集与编码"
echo.
echo.
pause
