"""
LangChain Agent 聊天应用主程序

这是一个基于 LangChain 的智能聊天助手，集成了时区查询等工具。
"""
import logging
import sys
from typing import NoReturn

from .config import AppConfig
from .agent import ChatAgent
from .utils import setup_logging, print_welcome, print_help, clear_screen

logger = logging.getLogger(__name__)


def run_chat_loop(agent: ChatAgent) -> NoReturn:
    """
    运行聊天循环
    
    Args:
        agent: 聊天代理实例
    """
    print_welcome()
    
    # 显示模型信息
    model_info = agent.get_model_info()
    logger.info(f"使用模型: {model_info['model']}")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n😊 You: ").strip()
            
            # 处理空输入
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！感谢使用！")
                sys.exit(0)
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'clear':
                clear_screen()
                print_welcome()
                continue
            
            # 处理正常对话
            try:
                response = agent.chat(user_input)
                print(f"\n🤖 AI: {response}")
            except Exception as e:
                logger.error(f"处理对话时出错: {e}")
                print(f"\n❌ 抱歉，处理您的请求时出错了: {e}")
        
        except KeyboardInterrupt:
            print("\n\n👋 检测到 Ctrl+C，正在退出...")
            sys.exit(0)
        
        except EOFError:
            print("\n\n👋 检测到 EOF，正在退出...")
            sys.exit(0)


def main() -> None:
    """主函数 - 应用入口点"""
    try:
        # 设置日志
        setup_logging(level="INFO")
        
        logger.info("正在启动 LangChain Agent 聊天系统...")
        
        # 加载配置
        config = AppConfig.from_env()
        
        # 创建代理
        agent = ChatAgent(config)
        
        # 运行聊天循环
        run_chat_loop(agent)
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}", exc_info=True)
        print(f"\n❌ 应用启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
