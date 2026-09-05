"""LangChain Agent 聊天应用"""

__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "A LangChain-based chat agent with tool integration"

from .agent import ChatAgent
from .config import AppConfig, LLMConfig, AgentConfig
from .tools import get_all_tools, get_current_time

__all__ = [
    "ChatAgent",
    "AppConfig",
    "LLMConfig", 
    "AgentConfig",
    "get_all_tools",
    "get_current_time",
]

