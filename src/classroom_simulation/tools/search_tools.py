"""
搜索工具模块

本模块提供网络搜索和知识库搜索工具，用于AI Agent获取教学资源：
- WebSearchTool: 使用DuckDuckGo进行网络搜索
- WebFetchTool: 从指定URL抓取网页内容
- KnowledgeSearchTool: 在本地知识库中搜索教学案例

作者: AI备课系统
版本: 2.0
"""

from crewai.tools import BaseTool
from pydantic import Field
from typing import Type
import requests
from bs4 import BeautifulSoup
import re


class WebSearchInput(BaseTool):
    """
    网络搜索输入参数类

    定义网络搜索时需要的输入参数：
    - query: 搜索关键词
    - max_results: 最大搜索结果数量（默认5条）
    """
    query: str = Field(..., description="搜索关键词")
    max_results: int = Field(default=5, description="最大搜索结果数量")


class WebSearchTool(BaseTool):
    """
    网络搜索工具

    功能：使用DuckDuckGo进行网络搜索，返回搜索结果摘要

    使用场景：
    - 搜索教学案例和教学资源
    - 搜索课标要求和教材解读
    - 获取最新的教学方法

    示例：
        tool = WebSearchTool()
        result = tool._run("Python数据分析 教学案例", max_results=3)
    """

    name: str = "web_search"
    description: str = "使用DuckDuckGo搜索网络信息，返回搜索结果摘要"
    args_schema: Type[WebSearchInput] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """
        执行网络搜索

        参数:
            query: str - 搜索关键词
            max_results: int - 最大搜索结果数量（默认5条）

        返回:
            str: 搜索结果列表，包含标题、链接、摘要
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return f"搜索请求失败：HTTP {response.status_code}"

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for result in soup.select(".result")[:max_results]:
                title_elem = result.select_one(".result__title a")
                snippet_elem = result.select_one(".result__snippet")

                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get("href", "")
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    results.append(f"标题: {title}\n链接: {link}\n摘要: {snippet}\n")

            if not results:
                return f"未找到与 '{query}' 相关的搜索结果"

            return f"搜索结果 ({query}):\n\n" + "\n---\n".join(results)
        except Exception as e:
            return f"搜索出错：{str(e)}"


class WebFetchInput(BaseTool):
    """
    网页抓取输入参数类

    定义网页抓取时需要的输入参数：
    - url: 要抓取的网页URL
    - max_length: 最大内容长度（默认5000字符）
    """
    url: str = Field(..., description="要抓取的网页URL")
    max_length: int = Field(default=5000, description="最大内容长度")


class WebFetchTool(BaseTool):
    """
    网页抓取工具

    功能：从指定URL抓取网页内容，提取文本摘要

    使用场景：
    - 抓取教学资源的详细内容
    - 获取公开课视频页面的描述信息
    - 提取教育网站的政策文件内容

    示例：
        tool = WebFetchTool()
        result = tool._run("https://example.com/article", max_length=3000)
    """

    name: str = "web_fetch"
    description: str = "从指定URL抓取网页内容，提取文本摘要"
    args_schema: Type[WebFetchInput] = WebFetchInput

    def _run(self, url: str, max_length: int = 5000) -> str:
        """
        抓取网页内容

        参数:
            url: str - 要抓取的网页URL
            max_length: int - 最大内容长度（默认5000字符）

        返回:
            str: 网页文本内容，如果失败则返回错误信息
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                return f"请求失败：HTTP {response.status_code}"

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r"\n{3,}", "\n\n", text)

            if len(text) > max_length:
                text = text[:max_length] + "\n\n...（内容已截断）"

            return f"网页内容 ({url}):\n\n{text}"
        except Exception as e:
            return f"抓取出错：{str(e)}"


class KnowledgeSearchInput(BaseTool):
    """
    知识库搜索输入参数类

    定义知识库搜索时需要的输入参数：
    - topic: 要搜索的教学主题/关键词
    - knowledge_dir: 知识库目录（默认 knowledge/agent）
    """
    topic: str = Field(..., description="要搜索的教学主题/关键词")
    knowledge_dir: str = Field(default="knowledge/agent", description="知识库目录")


class KnowledgeSearchTool(BaseTool):
    """
    知识库搜索工具

    功能：在本地教学案例知识库中搜索相关内容

    使用场景：
    - 搜索已有的教学案例
    - 查找同类课题的教学设计
    - 获取本地的教学资源

    示例：
        tool = KnowledgeSearchTool()
        result = tool._run("Python数据分析", "knowledge/agent")
    """

    name: str = "knowledge_search"
    description: str = "在本地教学案例知识库中搜索与主题相关的内容"
    args_schema: Type[KnowledgeSearchInput] = KnowledgeSearchInput

    def _run(self, topic: str, knowledge_dir: str = "knowledge/agent") -> str:
        """
        搜索知识库

        参数:
            topic: str - 要搜索的教学主题/关键词
            knowledge_dir: str - 知识库目录（默认 knowledge/agent）

        返回:
            str: 搜索结果列表，包含文件名、路径、内容预览
        """
        try:
            from pathlib import Path

            path = Path(knowledge_dir)
            if not path.exists():
                return f"错误：知识库目录不存在 - {knowledge_dir}"

            topic_lower = topic.lower()
            matches = []

            for md_file in path.rglob("*.md"):
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if topic_lower in content.lower() or topic_lower in md_file.name.lower():
                        preview = content[:500] if len(content) > 500 else content
                        preview = preview.replace("\n", " ")[:200]
                        matches.append(f"文件: {md_file.name}\n路径: {md_file}\n预览: {preview}...\n")
                except Exception:
                    continue

            if not matches:
                return f"知识库中未找到与 '{topic}' 相关的内容"

            return f"知识库搜索结果 (主题: {topic}):\n\n" + "\n---\n".join(matches[:10])
        except Exception as e:
            return f"知识库搜索出错：{str(e)}"