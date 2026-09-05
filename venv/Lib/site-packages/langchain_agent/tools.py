"""工具函数模块 - 定义 Agent 可用的工具"""
import logging
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
# NOTE:
# `StructuredTool` 实例在被 `@tool` 装饰后不再可直接调用。
# 为了同时满足 LangChain Agent 和单元测试的需求，我们保留原始函数供测试调用，
# 另行构建工具实例用于 Agent。
from langchain.tools import tool

logger = logging.getLogger(__name__)


def get_current_time(time_zone: str = "UTC") -> str:
    """
    获取指定时区的当前时间
    
    Args:
        time_zone: IANA 时区名称，例如 'UTC', 'Asia/Shanghai', 'America/New_York'
    
    Returns:
        格式化的时间字符串 (HH:MM:SS)
    
    Raises:
        ValueError: 当时区名称无效时
    """
    try:
        tz = ZoneInfo(time_zone)
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        logger.info(f"获取时区 {time_zone} 的当前时间: {current_time}")
        return current_time
    except ZoneInfoNotFoundError:
        error_msg = f"无效的时区名称: {time_zone}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        logger.error(f"获取时间时发生错误: {e}")
        raise


# 将函数包装成 LangChain 工具供 Agent 使用
get_current_time_tool = tool(get_current_time)


# 可以在这里添加更多工具
def get_all_tools() -> list:
    """
    返回所有可用的工具列表
    
    Returns:
        工具列表
    """
    return [get_current_time_tool]

