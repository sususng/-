"""
课堂模拟Crew - 模拟40分钟课堂教学

本模块负责课堂模拟流程，模拟真实的课堂教学场景：
- 主讲教师按照时间线进行40分钟模拟上课
- 三类学生（学优生、中等生、后进生）模拟不同层次学生的反应
- 听课教师进行课堂观察
- 教导主任和内容审核官进行审核

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

    确保AI生成的输出内容达到最低长度要求，避免输出内容过短。
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

    确保AI生成的输出符合Markdown文档格式要求，检查内容中是否包含标题标记。

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
class ClassDemoCrew:
    """
    课堂模拟Crew - 协调主教师、三类学生、听课教师、教导主任、内容审核官完成模拟上课

    本Crew模拟真实的课堂教学场景，包含以下角色：
    - leader_teacher: 高中信息技术主讲教师，按照时间线进行40分钟模拟上课
    - student_advanced: 学优生，快速反应，主动提问
    - student_intermediate: 中等生，按部就班，偶尔卡顿
    - student_basic: 后进生，需要更多帮助，容易出错
    - peer_teacher: 听课教师，进行课堂观察
    - academic_director: 教导主任，审核课堂模拟
    - content_auditor: 内容审核官，审核合规性

    课堂模拟流程采用顺序执行(sequential)，依次完成：
    1. 读取备课包
    2. 模拟上课
    3. 生成互动文件
    4. 学生反馈
    5. 听课教师观察
    6. 教导主任审核
    7. 内容审核官审核
    """

    agents_config = str(Path(__file__).parent / "config" / "agents.yaml")
    tasks_config = str(Path(__file__).parent / "config" / "tasks.yaml")

    @agent
    def leader_teacher(self) -> Agent:
        """
        创建主讲教师Agent

        主讲教师负责核心教学文件的生成和课堂模拟执行。
        配置较高的重试次数和最大迭代次数，确保复杂任务能够完成。
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

        听课教师负责课堂观察和反馈。
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

        教导主任负责审核课堂模拟文件的一致性、教师策略应用等。
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

    @agent
    def student_advanced(self) -> Agent:
        """
        创建学优生Agent

        学优生模拟编程基础扎实的学生特点：
        - 快速反应，主动提问
        - 能回答教师的问题链
        - 对新知识有强烈好奇心
        - 可能提出延伸问题
        """
        return Agent(
            config=self.agents_config["student_advanced"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @agent
    def student_intermediate(self) -> Agent:
        """
        创建中等生Agent

        中等生模拟能跟着操作但遇到变化会犹豫的学生特点：
        - 按部就班完成任务
        - 偶尔在计算时卡顿
        - 需要教师引导
        - 认真记录笔记
        """
        return Agent(
            config=self.agents_config["student_intermediate"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @agent
    def student_basic(self) -> Agent:
        """
        创建后进生Agent

        后进生模拟基础薄弱的学生特点：
        - 需要更多帮助
        - 可能在概念理解上有困难
        - 回答问题需要教师追问引导
        - 打字慢，容易出错
        """
        return Agent(
            config=self.agents_config["student_basic"],
            verbose=True,
            max_retry_limit=2,
            max_iter=5,
        )

    @task
    def read_prep_package(self) -> Task:
        """
        创建读取备课包任务

        任务描述：从备课包目录读取教案、PPT脚本、说课稿、资源清单、时间线等教学文件。
        """
        return Task(
            config=self.tasks_config["read_prep_package_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def simulate_class(self) -> Task:
        """
        创建模拟上课任务

        任务描述：按照课堂时间线进行40分钟模拟上课，应用教师主导策略。
        教师主导策略包括：
        - 设问-思考-追问
        - Q1-Q4层次问题链
        - 加工性反馈
        - 认知冲突类提问
        """
        return Task(
            config=self.tasks_config["simulate_class_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def generate_interaction_file(self) -> Task:
        """
        创建互动文件生成任务

        任务描述：根据模拟上课记录生成40分钟课堂模拟互动文件。
        输出内容包括：
        - 精确到秒的时间轴
        - 每个环节的开始和结束时间
        - 教师主导策略应用记录
        - 三类学生模拟特点
        - 边缘生关注记录
        """
        return Task(
            config=self.tasks_config["generate_interaction_file_task"],
            guardrail=markdown_format_guardrail,
        )

    @task
    def student_feedback(self) -> Task:
        """
        创建学优生反馈任务

        任务描述：学优生对课堂模拟互动文件提出反馈意见。
        """
        return Task(
            config=self.tasks_config["student_feedback_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def student_feedback_intermediate(self) -> Task:
        """
        创建中等生反馈任务

        任务描述：中等生对课堂模拟互动文件提出反馈意见。
        """
        return Task(
            config=self.tasks_config["student_feedback_intermediate_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def student_feedback_basic(self) -> Task:
        """
        创建后进生反馈任务

        任务描述：后进生对课堂模拟互动文件提出反馈意见。
        """
        return Task(
            config=self.tasks_config["student_feedback_basic_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def peer_observation(self) -> Task:
        """
        创建听课教师观察任务

        任务描述：听课教师基于课堂模拟互动文件进行观察和记录。
        观察要点包括：与教案一致性、提问等待时间、指令清晰度、师生互动等。
        """
        return Task(
            config=self.tasks_config["peer_observation_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def class_academic_audit(self) -> Task:
        """
        创建教导主任审核任务

        任务描述：教导主任审核课堂模拟互动文件。
        审核要点：与教案一致性、教师主导策略应用、学生模拟情况、边缘生关注记录。
        """
        return Task(
            config=self.tasks_config["class_academic_audit_task"],
            guardrail=output_length_guardrail,
        )

    @task
    def class_content_audit(self) -> Task:
        """
        创建内容合规性审核任务

        任务描述：内容审核官审核课堂模拟互动文件的合规性。
        审核要点：意识形态、科学性、适龄性、安全隐私。
        """
        return Task(
            config=self.tasks_config["class_content_audit_task"],
            guardrail=output_length_guardrail,
        )

    @crew
    def crew(self) -> Crew:
        """
        创建课堂模拟Crew

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