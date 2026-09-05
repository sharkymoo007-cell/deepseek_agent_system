"""Agent 模块 - 管理 LLM 和 Agent 的创建与交互"""
import logging
from typing import Dict, Any, Optional
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from .config import AppConfig
from .tools import get_all_tools

logger = logging.getLogger(__name__)


class ChatAgent:
    """聊天代理类 - 封装 LLM 和 Agent 的交互逻辑"""
    
    def __init__(self, config: AppConfig):
        """
        初始化聊天代理
        
        Args:
            config: 应用配置
        """
        self.config = config
        self._llm = None
        self._agent = None
        self._initialize()
    
    def _initialize(self) -> None:
        """初始化 LLM 和 Agent"""
        try:
            logger.info("初始化 LLM...")
            self._llm = self._create_llm()
            
            logger.info("初始化 Agent...")
            self._agent = self._create_agent()
            
            logger.info("Agent 初始化完成")
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            raise
    
    def _create_llm(self) -> ChatOllama:
        """
        创建 LLM 实例
        
        Returns:
            ChatOllama 实例
        """
        llm_config = self.config.llm
        return ChatOllama(
            model=llm_config.model,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens,
            top_p=llm_config.top_p,
            frequency_penalty=llm_config.frequency_penalty,
            presence_penalty=llm_config.presence_penalty,
            stop=None,
            stream=llm_config.stream,
            verbose=llm_config.verbose,
            api_key=llm_config.api_key,
        )
    
    def _create_agent(self):
        """
        创建 Agent 实例
        
        Returns:
            Agent 实例
        """
        tools = get_all_tools()
        return create_agent(
            model=self._llm,
            tools=tools,
            system_prompt=self.config.agent.system_prompt,
        )
    
    def chat(self, user_input: str) -> str:
        """
        处理用户输入并返回 AI 回复
        
        Args:
            user_input: 用户输入的消息
        
        Returns:
            AI 的回复内容
        
        Raises:
            Exception: 当处理消息时发生错误
        """
        try:
            logger.debug(f"用户输入: {user_input}")
            
            response = self._agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )
            
            # 获取最后一条消息（LLM 的最终回答）
            final_answer = response['messages'][-1].content
            
            logger.debug(f"AI 回复: {final_answer}")
            return final_answer
            
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            模型配置信息字典
        """
        return {
            "model": self.config.llm.model,
            "temperature": self.config.llm.temperature,
            "max_tokens": self.config.llm.max_tokens,
        }

