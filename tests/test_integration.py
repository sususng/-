import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestLessonPrepCrew:
    """测试备课Crew集成"""

    def test_lesson_prep_crew_initialization(self):
        """测试备课Crew初始化"""
        from classroom_simulation.crews.lesson_prep_crew import LessonPrepCrew
        
        crew = LessonPrepCrew()
        assert crew is not None
        assert hasattr(crew, 'crew')

    def test_lesson_prep_crew_has_required_agents(self):
        """测试备课Crew包含必需的Agent"""
        from classroom_simulation.crews.lesson_prep_crew import LessonPrepCrew
        
        crew = LessonPrepCrew()
        assert hasattr(crew, 'leader_teacher')
        assert hasattr(crew, 'peer_teacher')
        assert hasattr(crew, 'academic_director')
        assert hasattr(crew, 'content_auditor')

    def test_lesson_prep_crew_has_required_tasks(self):
        """测试备课Crew包含必需的Task"""
        from classroom_simulation.crews.lesson_prep_crew import LessonPrepCrew
        
        crew = LessonPrepCrew()
        assert hasattr(crew, 'search_resources')
        assert hasattr(crew, 'collaborative_prep')
        assert hasattr(crew, 'generate_lesson_plan')
        assert hasattr(crew, 'generate_ppt_script')
        assert hasattr(crew, 'generate_resource_list')
        assert hasattr(crew, 'generate_speech_script')
        assert hasattr(crew, 'generate_timeline')
        assert hasattr(crew, 'peer_review')
        assert hasattr(crew, 'academic_audit')
        assert hasattr(crew, 'content_audit')


class TestClassDemoCrew:
    """测试课堂模拟Crew集成"""

    def test_class_demo_crew_initialization(self):
        """测试课堂模拟Crew初始化"""
        from classroom_simulation.crews.class_demo_crew import ClassDemoCrew
        
        crew = ClassDemoCrew()
        assert crew is not None
        assert hasattr(crew, 'crew')

    def test_class_demo_crew_has_all_agents(self):
        """测试课堂模拟Crew包含全部7个Agent"""
        from classroom_simulation.crews.class_demo_crew import ClassDemoCrew
        
        crew = ClassDemoCrew()
        assert hasattr(crew, 'leader_teacher')
        assert hasattr(crew, 'peer_teacher')
        assert hasattr(crew, 'academic_director')
        assert hasattr(crew, 'content_auditor')
        assert hasattr(crew, 'student_advanced')
        assert hasattr(crew, 'student_intermediate')
        assert hasattr(crew, 'student_basic')

    def test_class_demo_crew_has_required_tasks(self):
        """测试课堂模拟Crew包含必需的Task"""
        from classroom_simulation.crews.class_demo_crew import ClassDemoCrew
        
        crew = ClassDemoCrew()
        assert hasattr(crew, 'read_prep_package')
        assert hasattr(crew, 'simulate_class')
        assert hasattr(crew, 'generate_interaction_file')
        assert hasattr(crew, 'student_feedback')
        assert hasattr(crew, 'student_feedback_intermediate')
        assert hasattr(crew, 'student_feedback_basic')
        assert hasattr(crew, 'peer_observation')
        assert hasattr(crew, 'class_academic_audit')
        assert hasattr(crew, 'class_content_audit')


class TestAgentIntegration:
    """测试Agent集成"""

    def test_leader_teacher_agent_class_exists(self):
        """测试主教师Agent类存在"""
        from classroom_simulation.agents.leader_teacher import LeaderTeacherAgent
        
        assert LeaderTeacherAgent is not None

    def test_peer_teacher_agent_class_exists(self):
        """测试听课教师Agent类存在"""
        from classroom_simulation.agents.peer_teacher import PeerTeacherAgent
        
        assert PeerTeacherAgent is not None

    def test_academic_director_agent_class_exists(self):
        """测试教导主任Agent类存在"""
        from classroom_simulation.agents.academic_director import AcademicDirectorAgent
        
        assert AcademicDirectorAgent is not None

    def test_content_auditor_agent_class_exists(self):
        """测试内容审核官Agent类存在"""
        from classroom_simulation.agents.content_auditor import ContentAuditorAgent
        
        assert ContentAuditorAgent is not None

    def test_student_agents_class_exists(self):
        """测试学生Agent类存在"""
        from classroom_simulation.agents.student_agents import StudentAgents
        
        assert StudentAgents is not None


class TestToolsIntegration:
    """测试工具集成"""

    def test_all_tools_can_be_imported(self):
        """测试所有工具可以被导入"""
        from classroom_simulation.tools import (
            FileReadTool,
            FileWriteTool,
            DirListTool,
            FileSearchTool,
            WebSearchTool,
            WebFetchTool,
            KnowledgeSearchTool,
            DocConvertTool,
            BatchConvertTool,
            LessonPlanTemplateTool,
            TimelineTemplateTool,
            InteractionTemplateTool,
        )
        
        assert FileReadTool is not None
        assert FileWriteTool is not None
        assert DirListTool is not None
        assert FileSearchTool is not None
        assert WebSearchTool is not None
        assert WebFetchTool is not None
        assert KnowledgeSearchTool is not None
        assert DocConvertTool is not None
        assert BatchConvertTool is not None
        assert LessonPlanTemplateTool is not None
        assert TimelineTemplateTool is not None
        assert InteractionTemplateTool is not None

    def test_lesson_plan_template_generates_complete_template(self):
        """测试教案模板生成完整模板"""
        from classroom_simulation.tools.template_tools import LessonPlanTemplateTool
        
        tool = LessonPlanTemplateTool()
        result = tool._run("数据采集与编码", "高一", 1)
        
        assert "# 教案 - 数据采集与编码" in result
        assert "基本信息" in result
        assert "课标要求" in result
        assert "教材分析" in result
        assert "学情分析" in result
        assert "教学目标" in result
        assert "教学重点" in result
        assert "教学难点" in result
        assert "教学过程" in result
        assert "课堂小结" in result
        assert "学生作业" in result
        assert "板书设计" in result
        assert "教学反思" in result

    def test_timeline_template_generates_complete_template(self):
        """测试时间线模板生成完整模板"""
        from classroom_simulation.tools.template_tools import TimelineTemplateTool
        
        tool = TimelineTemplateTool()
        result = tool._run("数据采集与编码", 40)
        
        assert "# 课堂时间线 - 数据采集与编码" in result
        assert "40分钟" in result
        assert "导入" in result
        assert "新授" in result
        assert "活动" in result
        assert "总结" in result
        assert "边缘生关注" in result

    def test_interaction_template_generates_complete_template(self):
        """测试互动模板生成完整模板"""
        from classroom_simulation.tools.template_tools import InteractionTemplateTool
        
        tool = InteractionTemplateTool()
        result = tool._run("数据采集与编码")
        
        assert "# 课堂模拟互动 - 数据采集与编码" in result
        assert "小智" in result
        assert "小程" in result
        assert "小新" in result
        assert "教师主导策略" in result


class TestConfigFiles:
    """测试配置文件"""

    def test_agents_config_exists(self):
        """测试agents配置文件存在"""
        from pathlib import Path
        
        config_path = Path(__file__).parent.parent / "src" / "classroom_simulation" / "config" / "agents.yaml"
        assert config_path.exists()

    def test_tasks_config_exists(self):
        """测试tasks配置文件存在"""
        from pathlib import Path
        
        config_path = Path(__file__).parent.parent / "src" / "classroom_simulation" / "config" / "tasks.yaml"
        assert config_path.exists()

    def test_agents_config_has_all_agents(self):
        """测试agents配置包含所有Agent"""
        from pathlib import Path
        import yaml
        
        config_path = Path(__file__).parent.parent / "src" / "classroom_simulation" / "config" / "agents.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        assert "leader_teacher" in config
        assert "peer_teacher" in config
        assert "academic_director" in config
        assert "content_auditor" in config
        assert "student_advanced" in config
        assert "student_intermediate" in config
        assert "student_basic" in config

    def test_tasks_config_has_required_tasks(self):
        """测试tasks配置包含必需的Task"""
        from pathlib import Path
        import yaml
        
        config_path = Path(__file__).parent.parent / "src" / "classroom_simulation" / "config" / "tasks.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        assert "search_resources_task" in config
        assert "generate_lesson_plan_task" in config
        assert "simulate_class_task" in config
        assert "student_feedback_task" in config
        assert "academic_audit_task" in config


class TestKnowledgeBase:
    """测试知识库"""

    def test_knowledge_base_directory_exists(self):
        """测试知识库目录存在"""
        from pathlib import Path
        
        knowledge_path = Path(__file__).parent.parent / "knowledge"
        assert knowledge_path.exists()

    def test_knowledge_base_has_cases(self):
        """测试知识库包含教学案例"""
        from pathlib import Path
        
        knowledge_path = Path(__file__).parent.parent / "knowledge" / "agent"
        if knowledge_path.exists():
            md_files = list(knowledge_path.rglob("*.md"))
            assert len(md_files) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
