"""
课堂模拟系统 - 教师AI备课与课堂模拟工具

本模块提供完整的AI辅助备课和课堂模拟功能：
- LessonPrepCrew: 备课流程Crew，协调主教师、听课教师、教导主任完成备课
- ClassDemoCrew: 课堂模拟Crew，模拟40分钟课堂教学

主要功能：
1. 备课流程：教案、PPT脚本、说课稿、时间线等教学文件生成
2. 课堂模拟：教师主导策略应用、学生模拟、师生互动模拟
3. 审核流程：听课教师审核、教导主任审核、内容审核官审核

作者: AI备课系统
版本: 2.0
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tasks.task_output import TaskOutput
from typing import List, Tuple, Any
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def output_length_guardrail(output: TaskOutput) -> Tuple[bool, Any]:
    """
    验证输出长度的守卫函数

    用于确保AI生成的输出内容达到最低长度要求，避免输出内容过短。
    如果输出内容少于100字符，返回验证失败。

    参数:
        output: TaskOutput - CrewAI任务输出对象

    返回:
        Tuple[bool, Any]: 验证结果和内容
        - (True, content): 验证通过
        - (False, error_message): 验证失败
    """
    content = output.result if hasattr(output, 'result') else str(output)
    if len(content) < 100:
        logger.warning(f"⚠️ 输出过短: {len(content)}字符")
        return (False, "输出内容过短，需要补充")
    return (True, content)


def markdown_format_guardrail(output: TaskOutput) -> Tuple[bool, Any]:
    """
    验证Markdown格式的守卫函数

    用于确保AI生成的输出符合Markdown文档格式要求。
    检查内容中是否包含标题标记(# 或 ##)。

    参数:
        output: TaskOutput - CrewAI任务输出对象

    返回:
        Tuple[bool, Any]: 验证结果和内容
        - (True, content): 验证通过
        - (False, error_message): 验证失败
    """
    content = output.result if hasattr(output, 'result') else str(output)
    if "#" not in content and "##" not in content:
        logger.warning("⚠️ 输出可能缺少Markdown标题")
        return (False, "缺少Markdown标题格式")
    return (True, content)


@CrewBase
class LessonPrepCrew:
    """
    备课Crew - 协调多角色Agent完成教学备课任务

    本Crew模拟真实的教研组备课场景，包含以下角色：
    - leader_teacher: 高中信息技术主讲教师，负责生成教案等核心教学文件
    - peer_teacher: 教研组同事，负责审核和提出改进建议
    - academic_director: 教导主任，负责教学专业审核
    - content_auditor: 教学内容审核官，负责合规性审核

    备课流程采用顺序执行(sequential)，确保每个文件都在前一个文件基础上生成。
    """

    agents_config = str(Path(__file__).parent / "config" / "agents.yaml")
    tasks_config = str(Path(__file__).parent / "config" / "tasks.yaml")

    @agent
    def leader_teacher(self) -> Agent:
        """
        创建主讲教师Agent

        主讲教师负责核心教学文件的生成，是备课流程的主要执行者。
        配置较高的重试次数(max_retry_limit=3)和最大迭代次数(max_iter=10)，
        确保复杂任务能够完成。
        """
        return Agent(
            config=self.agents_config["leader_teacher"],
            verbose=True,
            max_retry_limit=3,
            max_iter=10,
        )

    @agent
    def peer_teacher(self) -> Agent:
        """
        创建听课教师Agent

        听课教师负责审核和反馈，提供教学视角的评审意见。
        配置适中的重试次数和迭代次数。
        """
        return Agent(
            config=self.agents_config["peer_teacher"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @agent
    def academic_director(self) -> Agent:
        """
        创建教导主任Agent

        教导主任负责最终的教学专业审核，从六维度评估教学质量。
        配置适中的重试次数和迭代次数。
        """
        return Agent(
            config=self.agents_config["academic_director"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @agent
    def content_auditor(self) -> Agent:
        """
        创建内容审核官Agent

        内容审核官负责合规性审核，确保教学内容符合教育规范。
        配置较低的重试次数和迭代次数。
        """
        return Agent(
            config=self.agents_config["content_auditor"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @task
    def search_resources(self) -> Task:
        """
        创建资源搜索任务

        任务描述：从本地知识库和互联网搜索与课题相关的教学案例和资源。
        """
        return Task(
            config=self.tasks_config["search_resources_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_resource_list(self) -> Task:
        """
        创建教学资源清单生成任务

        任务描述：根据搜索结果整理多媒体资源、软件工具、在线资源、学生素材四类资源。
        """
        return Task(
            config=self.tasks_config["generate_resource_list_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def peer_review_resource_list(self) -> Task:
        """
        创建资源清单审核任务

        任务描述：听课教师审核资源清单的完整性、适用性、可替代性、可行性。
        """
        return Task(
            config=self.tasks_config["peer_review_resource_list_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_lesson_plan(self) -> Task:
        """
        创建教案生成任务

        任务描述：基于资源清单和案例生成完整教案，包含教学目标、重难点、教学过程、教学反思。
        教学过程必须包含教师活动、学生活动、教学意图三列。
        """
        return Task(
            config=self.tasks_config["generate_lesson_plan_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def peer_review_lesson_plan(self) -> Task:
        """
        创建教案审核任务

        任务描述：听课教师审核教案的教学目标可测性、时间分配合理性、作业分层等。
        """
        return Task(
            config=self.tasks_config["peer_review_lesson_plan_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_ppt_script(self) -> Task:
        """
        创建PPT脚本生成任务

        任务描述：根据教案和资源清单生成PPT脚本，包含每页的标题、内容要点、动画建议等。
        """
        return Task(
            config=self.tasks_config["generate_ppt_script_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def peer_review_ppt_script(self) -> Task:
        """
        创建PPT脚本审核任务

        任务描述：听课教师审核PPT脚本的内容一致性、页面设计、动画互动设计。
        """
        return Task(
            config=self.tasks_config["peer_review_ppt_script_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_speech_script(self) -> Task:
        """
        创建说课稿生成任务

        任务描述：根据教案和PPT脚本生成教师逐字说课稿，包含说教材、学情、教法、学法、教学过程、板书。
        """
        return Task(
            config=self.tasks_config["generate_speech_script_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def peer_review_speech_script(self) -> Task:
        """
        创建说课稿审核任务

        任务描述：听课教师审核说课稿的语言表达、意图说明、时间安排。
        """
        return Task(
            config=self.tasks_config["peer_review_speech_script_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_timeline(self) -> Task:
        """
        创建课堂时间线生成任务

        任务描述：根据教案、PPT脚本和说课稿生成课堂时间线，时间精确到秒，包含边缘生关注节点。
        """
        return Task(
            config=self.tasks_config["generate_timeline_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def peer_review_timeline(self) -> Task:
        """
        创建时间线审核任务

        任务描述：听课教师审核时间线的时间分配合理性、内容一致性、边缘生关注。
        """
        return Task(
            config=self.tasks_config["peer_review_timeline_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def academic_audit(self) -> Task:
        """
        创建教导主任教学专业审核任务

        任务描述：教导主任从六维度(学习目标、学习内容、教学策略、学习参与、学习反馈、技术融合)审核全部备课文件。
        """
        return Task(
            config=self.tasks_config["academic_audit_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def content_audit(self) -> Task:
        """
        创建内容合规性审核任务

        任务描述：内容审核官从四大维度(意识形态、科学性、适龄性、安全隐私)审核全部备课文件。
        """
        return Task(
            config=self.tasks_config["content_audit_task"],
            guardrail=output_length_guardrail,
        )

    @crew
    def crew(self) -> Crew:
        """
        创建备课Crew

        返回配置好的Crew对象，采用顺序执行流程，支持verbose日志输出。

        返回:
            Crew: 配置完成的Crew对象，可用于执行kickoff
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
        )