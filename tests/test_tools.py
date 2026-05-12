import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestFileTools:
    """测试文件读写工具"""

    def test_file_read_tool_exists(self):
        """测试文件读取工具是否存在"""
        from classroom_simulation.tools.file_tools import FileReadTool
        tool = FileReadTool()
        assert tool.name == "file_read"
        assert "读取" in tool.description

    def test_file_write_tool_exists(self):
        """测试文件写入工具是否存在"""
        from classroom_simulation.tools.file_tools import FileWriteTool
        tool = FileWriteTool()
        assert tool.name == "file_write"
        assert "写入" in tool.description

    def test_dir_list_tool_exists(self):
        """测试目录列表工具是否存在"""
        from classroom_simulation.tools.file_tools import DirListTool
        tool = DirListTool()
        assert tool.name == "dir_list"
        assert "目录" in tool.description

    def test_file_search_tool_exists(self):
        """测试文件搜索工具是否存在"""
        from classroom_simulation.tools.file_tools import FileSearchTool
        tool = FileSearchTool()
        assert tool.name == "file_search"
        assert "搜索" in tool.description

    def test_file_write_and_read(self, tmp_path):
        """测试文件写入和读取"""
        from classroom_simulation.tools.file_tools import FileWriteTool, FileReadTool
        
        test_file = tmp_path / "test.md"
        test_content = "# 测试文件\n\n这是测试内容"
        
        write_tool = FileWriteTool()
        result = write_tool._run(str(test_file), test_content)
        assert "成功" in result
        
        read_tool = FileReadTool()
        content = read_tool._run(str(test_file))
        assert "测试文件" in content
        assert "测试内容" in content


class TestSearchTools:
    """测试搜索工具"""

    def test_web_search_tool_exists(self):
        """测试网络搜索工具是否存在"""
        from classroom_simulation.tools.search_tools import WebSearchTool
        tool = WebSearchTool()
        assert tool.name == "web_search"
        assert "搜索" in tool.description

    def test_web_fetch_tool_exists(self):
        """测试网页抓取工具是否存在"""
        from classroom_simulation.tools.search_tools import WebFetchTool
        tool = WebFetchTool()
        assert tool.name == "web_fetch"
        assert "抓取" in tool.description

    def test_knowledge_search_tool_exists(self):
        """测试知识库搜索工具是否存在"""
        from classroom_simulation.tools.search_tools import KnowledgeSearchTool
        tool = KnowledgeSearchTool()
        assert tool.name == "knowledge_search"
        assert "知识库" in tool.description


class TestDocConverter:
    """测试文档转换工具"""

    def test_doc_convert_tool_exists(self):
        """测试文档转换工具是否存在"""
        from classroom_simulation.tools.doc_converter import DocConvertTool
        tool = DocConvertTool()
        assert tool.name == "doc_convert"
        assert "转换" in tool.description

    def test_batch_convert_tool_exists(self):
        """测试批量转换工具是否存在"""
        from classroom_simulation.tools.doc_converter import BatchConvertTool
        tool = BatchConvertTool()
        assert tool.name == "batch_convert"
        assert "批量" in tool.description

    def test_doc_convert_unsupported_format(self, tmp_path):
        """测试不支持的格式"""
        from classroom_simulation.tools.doc_converter import DocConvertTool
        
        tool = DocConvertTool()
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        result = tool._run(str(test_file))
        assert "错误" in result or "不支持" in result


class TestTemplateTools:
    """测试模板生成工具"""

    def test_lesson_plan_template_exists(self):
        """测试教案模板工具是否存在"""
        from classroom_simulation.tools.template_tools import LessonPlanTemplateTool
        tool = LessonPlanTemplateTool()
        assert tool.name == "lesson_plan_template"
        assert "教案" in tool.description

    def test_timeline_template_exists(self):
        """测试时间线模板工具是否存在"""
        from classroom_simulation.tools.template_tools import TimelineTemplateTool
        tool = TimelineTemplateTool()
        assert tool.name == "timeline_template"
        assert "时间线" in tool.description

    def test_interaction_template_exists(self):
        """测试互动模板工具是否存在"""
        from classroom_simulation.tools.template_tools import InteractionTemplateTool
        tool = InteractionTemplateTool()
        assert tool.name == "interaction_template"
        assert "互动" in tool.description

    def test_lesson_plan_template_content(self):
        """测试教案模板内容"""
        from classroom_simulation.tools.template_tools import LessonPlanTemplateTool
        
        tool = LessonPlanTemplateTool()
        result = tool._run("测试课题", "高一", 1)
        
        assert "测试课题" in result
        assert "基本信息" in result
        assert "课标要求" in result
        assert "教学目标" in result
        assert "教学过程" in result

    def test_timeline_template_content(self):
        """测试时间线模板内容"""
        from classroom_simulation.tools.template_tools import TimelineTemplateTool
        
        tool = TimelineTemplateTool()
        result = tool._run("测试课题", 40)
        
        assert "测试课题" in result
        assert "40分钟" in result
        assert "导入" in result
        assert "新授" in result
        assert "活动" in result
        assert "总结" in result

    def test_interaction_template_content(self):
        """测试互动模板内容"""
        from classroom_simulation.tools.template_tools import InteractionTemplateTool
        
        tool = InteractionTemplateTool()
        result = tool._run("测试课题")
        
        assert "测试课题" in result
        assert "学生优" in result
        assert "学生中" in result
        assert "学生差" in result
        assert "小智" in result
        assert "小程" in result
        assert "小新" in result


class TestAgents:
    """测试Agent定义"""

    def test_leader_teacher_agent_exists(self):
        """测试主教师Agent是否存在"""
        from classroom_simulation.agents.leader_teacher import LeaderTeacherAgent
        assert LeaderTeacherAgent is not None

    def test_peer_teacher_agent_exists(self):
        """测试听课教师Agent是否存在"""
        from classroom_simulation.agents.peer_teacher import PeerTeacherAgent
        assert PeerTeacherAgent is not None

    def test_academic_director_agent_exists(self):
        """测试教导主任Agent是否存在"""
        from classroom_simulation.agents.academic_director import AcademicDirectorAgent
        assert AcademicDirectorAgent is not None

    def test_content_auditor_agent_exists(self):
        """测试内容审核官Agent是否存在"""
        from classroom_simulation.agents.content_auditor import ContentAuditorAgent
        assert ContentAuditorAgent is not None

    def test_student_agents_exist(self):
        """测试学生Agent是否存在"""
        from classroom_simulation.agents.student_agents import StudentAgents
        assert StudentAgents is not None


class TestCrews:
    """测试Crew定义"""

    def test_lesson_prep_crew_exists(self):
        """测试备课Crew是否存在"""
        from classroom_simulation.crews.lesson_prep_crew import LessonPrepCrew
        assert LessonPrepCrew is not None

    def test_class_demo_crew_exists(self):
        """测试课堂模拟Crew是否存在"""
        from classroom_simulation.crews.class_demo_crew import ClassDemoCrew
        assert ClassDemoCrew is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
