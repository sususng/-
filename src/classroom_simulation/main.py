#!/usr/bin/env python
import sys
import warnings
import argparse
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path)

from classroom_simulation.crews import LessonPrepCrew, ClassDemoCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Timer:
    """计时器类"""
    def __init__(self):
        self.start_time = None
        self.checkpoints = []
        self.current_checkpoints = {}
    
    def start(self, name: str = "主流程"):
        """开始计时"""
        self.start_time = time.time()
        self.checkpoints = []
        self.current_checkpoints = {}
        print(f"\n{'='*60}")
        print(f"⏱️ 开始计时 - {name}")
        print(f"{'='*60}")
        return self
    
    def checkpoint(self, name: str):
        """记录检查点"""
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
        
        elapsed = current_time - self.start_time
        self.checkpoints.append({
            "name": name,
            "elapsed": elapsed,
            "timestamp": current_time
        })
        self.current_checkpoints[name] = elapsed
        return elapsed
    
    def get_elapsed(self) -> float:
        """获取已用时间"""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def report(self, name: str) -> float:
        """报告当前步骤用时"""
        elapsed = self.get_elapsed()
        last_checkpoint = self.checkpoints[-1] if self.checkpoints else None
        step_time = 0
        if last_checkpoint:
            step_time = elapsed - (self.checkpoints[-2]["elapsed"] if len(self.checkpoints) > 1 else 0)
        
        print(f"\n📊 步骤完成: {name}")
        print(f"   本步骤用时: {step_time:.1f}秒 ({step_time/60:.1f}分钟)")
        print(f"   累计用时: {elapsed:.1f}秒 ({elapsed/60:.1f}分钟)")
        return step_time
    
    def report_total(self, name: str = "主流程"):
        """报告总用时"""
        total = self.get_elapsed()
        print(f"\n{'='*60}")
        print(f"🏁 {name}完成!")
        print(f"   总用时: {total:.1f}秒 ({total/60:.1f}分钟)")
        if total > 60:
            print(f"   约等于: {total/60:.2f}分钟")
        print(f"{'='*60}\n")
        
        if self.checkpoints:
            print(f"\n📋 用时明细:")
            for i, cp in enumerate(self.checkpoints):
                step_time = cp["elapsed"] - (self.checkpoints[i-1]["elapsed"] if i > 0 else 0)
                print(f"   {i+1}. {cp['name']}: {step_time:.1f}秒")
        
        return total


# 全局计时器
timer = Timer()


def run_lesson_prep(topic: str, output_dir: str = None):
    """
    运行备课流程
    """
    global timer
    
    if not output_dir:
        output_dir = f"output/{topic}"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"开始备课 - 主题: {topic}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*60}\n")
    
    timer.start(f"备课流程 - {topic}")
    timer.checkpoint("初始化")
    
    try:
        logger.info("初始化LessonPrepCrew")
        crew = LessonPrepCrew()
        timer.report("初始化")
        timer.checkpoint("资源搜索")
        
        result = crew.crew().kickoff(inputs={
            "topic": topic,
            "output_dir": output_dir,
            "current_year": str(datetime.now().year)
        })
        
        timer.report("资源搜索")
        timer.checkpoint("教学资源清单")
        
        logger.info(f"备课完成 - 结果保存在: {output_dir}")
        timer.report("教学资源清单")
        
        print(f"\n{'='*60}")
        print(f"备课完成!")
        print(f"结果保存在: {output_dir}")
        print(f"{'='*60}\n")
        
        timer.report_total(f"备课流程 - {topic}")
        return result
    except Exception as e:
        logger.error(f"备课出错: {str(e)}", exc_info=True)
        print(f"备课出错: {e}")
        timer.report("错误")
        raise


def run_class_demo(prep_package: str, output_dir: str = None):
    """
    运行课堂模拟流程
    """
    global timer
    topic = Path(prep_package).name
    
    logger.info(f"开始课堂模拟流程 - 备课包: {prep_package}")
    
    if not output_dir:
        output_dir = prep_package
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"开始课堂模拟 - 备课包: {prep_package}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*60}\n")
    
    timer.start(f"课堂模拟流程 - {topic}")
    timer.checkpoint("初始化")
    
    try:
        logger.info("初始化ClassDemoCrew")
        crew = ClassDemoCrew()
        timer.report("初始化")
        timer.checkpoint("读取备课包")
        
        result = crew.crew().kickoff(inputs={
            "topic": topic,
            "prep_package": prep_package,
            "output_dir": output_dir,
            "current_year": str(datetime.now().year)
        })
        
        timer.report("读取备课包")
        logger.info(f"课堂模拟完成 - 结果保存在: {output_dir}")
        
        print(f"\n{'='*60}")
        print(f"课堂模拟完成!")
        print(f"结果保存在: {output_dir}")
        print(f"{'='*60}\n")
        
        timer.report_total(f"课堂模拟流程 - {topic}")
        return result
    except Exception as e:
        logger.error(f"课堂模拟出错: {str(e)}", exc_info=True)
        print(f"课堂模拟出错: {e}")
        timer.report("错误")
        raise


def run():
    """
    运行备课流程（默认）
    """
    parser = argparse.ArgumentParser(description="课堂模拟CrewAIv2")
    parser.add_argument("--topic", "-t", type=str, default="数据采集与编码", help="备课主题")
    parser.add_argument("--output", "-o", type=str, default=None, help="输出目录")
    parser.add_argument("--mode", "-m", type=str, default="prep", choices=["prep", "demo"], help="运行模式: prep=备课, demo=课堂模拟")
    parser.add_argument("--prep-package", "-p", type=str, default=None, help="备课包路径（课堂模拟模式）")
    
    args = parser.parse_args()
    
    if args.mode == "prep":
        run_lesson_prep(args.topic, args.output)
    else:
        if not args.prep_package:
            print("课堂模拟模式需要指定 --prep-package 或 -p 参数")
            return
        run_class_demo(args.prep_package, args.output)


def test_all_tools():
    """测试所有工具"""
    global timer
    timer.start("工具测试")
    
    logger.info("开始测试工具集")
    print("\n测试工具集...\n")
    
    from classroom_simulation.tools import (
        FileReadTool, FileWriteTool, DirListTool, FileSearchTool,
        WebSearchTool, WebFetchTool, KnowledgeSearchTool,
        DocConvertTool, BatchConvertTool,
        LessonPlanTemplateTool, TimelineTemplateTool, InteractionTemplateTool,
    )
    
    tools = [
        ("FileReadTool", FileReadTool),
        ("FileWriteTool", FileWriteTool),
        ("DirListTool", DirListTool),
        ("FileSearchTool", FileSearchTool),
        ("WebSearchTool", WebSearchTool),
        ("WebFetchTool", WebFetchTool),
        ("KnowledgeSearchTool", KnowledgeSearchTool),
        ("DocConvertTool", DocConvertTool),
        ("BatchConvertTool", BatchConvertTool),
        ("LessonPlanTemplateTool", LessonPlanTemplateTool),
        ("TimelineTemplateTool", TimelineTemplateTool),
        ("InteractionTemplateTool", InteractionTemplateTool),
    ]
    
    success_count = 0
    fail_count = 0
    for name, tool_class in tools:
        try:
            tool = tool_class()
            print(f"✅ {name} - OK")
            logger.info(f"工具测试通过: {name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {name} - {e}")
            logger.error(f"工具测试失败: {name} - {str(e)}")
            fail_count += 1
    
    logger.info(f"工具测试完成 - 成功: {success_count}, 失败: {fail_count}")
    print(f"\n工具测试完成 - 成功: {success_count}, 失败: {fail_count}\n")
    
    timer.report_total("工具测试")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-tools":
        test_all_tools()
    else:
        run()
