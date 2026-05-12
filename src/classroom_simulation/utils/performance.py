from functools import wraps
import time
import logging
from typing import Callable, Any
from pathlib import Path
import hashlib
import json

logger = logging.getLogger(__name__)


class CacheManager:
    """缓存管理器 - 提高重复操作的性能"""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, key: str) -> str:
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key: str) -> Any:
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def set(self, key: str, value: Any) -> None:
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(value, f, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")

    def clear(self) -> None:
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception:
                pass


def timing_decorator(func: Callable) -> Callable:
    """计时装饰器 - 监控函数执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} 执行耗时: {elapsed:.2f}秒")
        return result
    return wrapper


def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器 - 失败时自动重试"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"{func.__name__} 第{attempt+1}次失败: {e}, {delay}秒后重试")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics = {}

    def record(self, name: str, value: float) -> None:
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def get_stats(self, name: str) -> dict:
        if name not in self.metrics or not self.metrics[name]:
            return {}
        values = self.metrics[name]
        return {
            "count": len(values),
            "total": sum(values),
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values)
        }

    def report(self) -> str:
        lines = ["性能报告:"]
        for name, values in self.metrics.items():
            if values:
                stats = self.get_stats(name)
                lines.append(f"  {name}: 平均{stats['average']:.2f}秒, 共{stats['count']}次")
        return "\n".join(lines)
