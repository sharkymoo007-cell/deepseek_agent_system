"""工具函数模块 - 提供通用工具函数"""
import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    配置日志系统
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 可选的日志文件路径
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 基本配置
    handlers = [logging.StreamHandler(sys.stdout)]
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
    )


def print_welcome() -> None:
    """打印欢迎信息"""
    welcome_text = """
╔══════════════════════════════════════════════════════════╗
║          欢迎使用 LangChain Agent 聊天系统              ║
║                                                          ║
║  输入 'quit', 'exit' 或 'q' 退出程序                    ║
║  输入 'help' 查看帮助信息                                ║
╚══════════════════════════════════════════════════════════╝
"""
    print(welcome_text)


def print_help() -> None:
    """打印帮助信息"""
    help_text = """
可用命令:
  quit/exit/q  - 退出程序
  help         - 显示此帮助信息
  clear        - 清空屏幕
  
示例问题:
  - What's the current time in Tokyo?
  - 北京现在几点了?
  - Get the current time in America/New_York
"""
    print(help_text)


def clear_screen() -> None:
    """清空屏幕"""
    import os
    os.system('clear' if os.name != 'nt' else 'cls')

