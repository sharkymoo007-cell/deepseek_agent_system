"""配置文件 - 集中管理应用配置"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """LLM 配置"""
    model: str = "gpt-oss"
    temperature: float = 0.0
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stream: bool = False
    verbose: bool = False
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """从环境变量加载配置"""
        return cls(
            model=os.getenv("LLM_MODEL", cls.model),
            temperature=float(os.getenv("LLM_TEMPERATURE", cls.temperature)),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", cls.max_tokens)),
            verbose=os.getenv("LLM_VERBOSE", "false").lower() == "true",
            api_key=os.getenv("LLM_API_KEY"),
        )


@dataclass
class AgentConfig:
    """Agent 配置"""
    system_prompt: str = "You are a helpful assistant that can answer questions and help with tasks."

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """从环境变量加载配置"""
        return cls(
            system_prompt=os.getenv("AGENT_SYSTEM_PROMPT", cls.system_prompt)
        )


@dataclass
class AppConfig:
    """应用配置"""
    llm: LLMConfig
    agent: AgentConfig

    @classmethod
    def from_env(cls) -> "AppConfig":
        """从环境变量加载所有配置"""
        return cls(
            llm=LLMConfig.from_env(),
            agent=AgentConfig.from_env(),
        )

