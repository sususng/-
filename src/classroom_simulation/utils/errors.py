import logging
from typing import Optional, Any, Dict
from pathlib import Path
import traceback

logger = logging.getLogger(__name__)


class ClassroomSimulationError(Exception):
    """课堂模拟基础异常类"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AgentError(ClassroomSimulationError):
    """Agent相关错误"""
    pass


class TaskError(ClassroomSimulationError):
    """Task相关错误"""
    pass


class FileError(ClassroomSimulationError):
    """文件操作错误"""
    pass


class ConfigError(ClassroomSimulationError):
    """配置错误"""
    pass


class LLMError(ClassroomSimulationError):
    """LLM调用错误"""
    pass


class ErrorHandler:
    """错误处理器"""

    def __init__(self, error_log_file: Optional[str] = None):
        self.error_log_file = error_log_file
        if error_log_file:
            self.log_path = Path(error_log_file)
            self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def handle(self, error: Exception, context: Optional[Dict] = None) -> str:
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "context": context or {},
        }
        
        if self.error_log_file:
            self._log_error(error_info)
        
        logger.error(f"错误: {error_info['type']} - {error_info['message']}")
        
        return self.format_error_message(error_info)

    def _log_error(self, error_info: Dict) -> None:
        try:
            import json
            from datetime import datetime
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                **error_info
            }
            
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning(f"错误日志写入失败: {e}")

    def format_error_message(self, error_info: Dict) -> str:
        if isinstance(error_info.get("type"), AgentError):
            return f"Agent错误: {error_info['message']}"
        elif isinstance(error_info.get("type"), TaskError):
            return f"任务错误: {error_info['message']}"
        elif isinstance(error_info.get("type"), FileError):
            return f"文件错误: {error_info['message']}"
        elif isinstance(error_info.get("type"), ConfigError):
            return f"配置错误: {error_info['message']}"
        elif isinstance(error_info.get("type"), LLMError):
            return f"LLM调用错误: {error_info['message']}"
        else:
            return f"错误: {error_info['message']}"


def safe_execute(func):
    """安全执行装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClassroomSimulationError as e:
            logger.error(f"业务错误: {e.message}")
            return {"error": e.message, "details": e.details}
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            logger.debug(traceback.format_exc())
            return {"error": "系统错误", "message": str(e)}
    return wrapper


class ValidationError(Exception):
    """验证错误"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


def validate_file_path(path: str) -> bool:
    """验证文件路径"""
    if not path:
        raise ValidationError("path", "文件路径不能为空")
    if len(path) > 260:
        raise ValidationError("path", "文件路径过长")
    return True


def validate_agent_config(config: Dict) -> bool:
    """验证Agent配置"""
    required_fields = ["role", "goal"]
    for field in required_fields:
        if field not in config:
            raise ValidationError("config", f"缺少必需字段: {field}")
    return True


def validate_task_config(config: Dict) -> bool:
    """验证Task配置"""
    required_fields = ["description", "expected_output"]
    for field in required_fields:
        if field not in config:
            raise ValidationError("config", f"缺少必需字段: {field}")
    return True
