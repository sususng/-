"""
文件操作工具模块

本模块提供文件系统操作工具，用于AI Agent读取和写入教学文件：
- FileReadTool: 读取文件内容
- FileWriteTool: 写入文件内容
- DirListTool: 列出目录内容
- FileSearchTool: 在目录中搜索文件

作者: AI备课系统
版本: 2.0
"""

from crewai.tools import BaseTool
from pydantic import Field
from typing import Type
from pathlib import Path


class ReadInput(BaseTool):
    """
    文件读取输入参数类

    定义读取文件时需要的输入参数：
    - file_path: 要读取的文件路径
    """
    file_path: str = Field(..., description="要读取的文件路径")


class FileReadTool(BaseTool):
    """
    文件读取工具

    功能：读取指定路径的文件内容，支持.md、.txt等文本文件

    使用场景：
    - AI Agent读取备课包中的教案、PPT脚本等文件
    - 读取知识库中的教学案例
    - 读取配置文件

    示例：
        tool = FileReadTool()
        result = tool._run("output/教案.md")
    """

    name: str = "file_read"
    description: str = "读取指定路径的文件内容，支持.md、.txt等文本文件"
    args_schema: Type[ReadInput] = ReadInput

    def _run(self, file_path: str) -> str:
        """
        读取文件内容

        参数:
            file_path: str - 要读取的文件路径

        返回:
            str: 文件内容，如果读取失败则返回错误信息
        """
        try:
            path = Path(file_path)

            if not path.exists():
                return f"错误：文件不存在 - {file_path}"

            if path.is_dir():
                return f"错误：路径是目录而非文件 - {file_path}"

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            return f"文件内容 ({file_path}):\n\n{content}"
        except Exception as e:
            return f"读取文件出错：{str(e)}"


class WriteInput(BaseTool):
    """
    文件写入输入参数类

    定义写入文件时需要的输入参数：
    - file_path: 要写入的文件路径
    - content: 要写入的内容
    """
    file_path: str = Field(..., description="要写入的文件路径")
    content: str = Field(..., description="要写入的内容")


class FileWriteTool(BaseTool):
    """
    文件写入工具

    功能：将内容写入指定路径的文件，支持创建.md、.txt等文本文件

    使用场景：
    - AI Agent生成教案后保存到文件
    - 生成PPT脚本、说课稿等教学文件
    - 保存课堂模拟结果

    示例：
        tool = FileWriteTool()
        result = tool._run("output/教案.md", "# 教案\n\n内容...")
    """

    name: str = "file_write"
    description: str = "将内容写入指定路径的文件，支持创建.md、.txt等文本文件"
    args_schema: Type[WriteInput] = WriteInput

    def _run(self, file_path: str, content: str) -> str:
        """
        写入文件内容

        参数:
            file_path: str - 要写入的文件路径
            content: str - 要写入的内容

        返回:
            str: 操作结果，如果成功则返回成功信息，失败则返回错误信息
        """
        try:
            path = Path(file_path)

            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"成功写入文件：{file_path}"
        except Exception as e:
            return f"写入文件出错：{str(e)}"


class ListDirInput(BaseTool):
    """
    目录列表输入参数类

    定义列出目录时需要的输入参数：
    - dir_path: 要列出的目录路径（默认当前目录）
    """
    dir_path: str = Field(default=".", description="要列出的目录路径")


class DirListTool(BaseTool):
    """
    目录列表工具

    功能：列出指定目录下的所有文件和子目录

    使用场景：
    - 查看备课包目录结构
    - 查看输出目录中的文件列表
    - 浏览知识库目录

    示例：
        tool = DirListTool()
        result = tool._run("output/Python数据分析")
    """

    name: str = "dir_list"
    description: str = "列出指定目录下的所有文件和子目录"
    args_schema: Type[ListDirInput] = ListDirInput

    def _run(self, dir_path: str = ".") -> str:
        """
        列出目录内容

        参数:
            dir_path: str - 要列出的目录路径（默认当前目录）

        返回:
            str: 目录内容列表，如果失败则返回错误信息
        """
        try:
            path = Path(dir_path)

            if not path.exists():
                return f"错误：目录不存在 - {dir_path}"

            if not path.is_dir():
                return f"错误：路径不是目录 - {dir_path}"

            items = []
            for item in sorted(path.iterdir()):
                item_type = "📁 目录" if item.is_dir() else "📄 文件"
                items.append(f"{item_type}: {item.name}")

            if not items:
                return f"目录为空：{dir_path}"

            return f"目录内容 ({dir_path}):\n\n" + "\n".join(items)
        except Exception as e:
            return f"列出目录出错：{str(e)}"


class SearchFilesInput(BaseTool):
    """
    文件搜索输入参数类

    定义搜索文件时需要的输入参数：
    - dir_path: 要搜索的目录路径（默认当前目录）
    - pattern: 文件名匹配模式
    """
    dir_path: str = Field(default=".", description="要在哪个目录搜索")
    pattern: str = Field(..., description="文件名模式，如 .md, 教案, 信息技术")


class FileSearchTool(BaseTool):
    """
    文件搜索工具

    功能：在指定目录中搜索匹配文件名模式的文件

    使用场景：
    - 搜索备课包中的教案文件
    - 在知识库中搜索特定主题的教学案例
    - 查找特定格式的文件

    示例：
        tool = FileSearchTool()
        result = tool._run("output", "教案")
    """

    name: str = "file_search"
    description: str = "在指定目录中搜索匹配文件名模式的文件"
    args_schema: Type[SearchFilesInput] = SearchFilesInput

    def _run(self, dir_path: str = ".", pattern: str = "") -> str:
        """
        搜索文件

        参数:
            dir_path: str - 要搜索的目录路径（默认当前目录）
            pattern: str - 文件名匹配模式

        返回:
            str: 搜索结果列表，如果失败则返回错误信息
        """
        try:
            path = Path(dir_path)

            if not path.exists():
                return f"错误：目录不存在 - {dir_path}"

            if not pattern:
                return "错误：请提供搜索模式"

            pattern_lower = pattern.lower()
            matches = []

            for item in path.rglob("*"):
                if item.is_file() and pattern_lower in item.name.lower():
                    matches.append(f"📄 {item.relative_to(path)}")

            if not matches:
                return f"未找到匹配 '{pattern}' 的文件"

            return f"搜索结果 (模式: {pattern}):\n\n" + "\n".join(matches)
        except Exception as e:
            return f"搜索文件出错：{str(e)}"