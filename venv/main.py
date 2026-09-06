import os
import sys
from dotenv import load_dotenv
from simpleeval import simple_eval
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# 1. Verify environment parameters(API KEY)
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("ERROR[not found]: Unable to find env var DEEPSEEK_API_KEY, please define!")
    sys.exit(1)

tavily_key = os.getenv("TAVILY_API_KEY")
if not tavily_key:
    print("WARNING[not found]: TAVILY_API_KEY not found in environment. Web search may fail if called.")

# 2. Define Agent Toolbox
@tool
def calculate(expression: str) -> str:
    """math operation calculation. example: '(100 - 32) / 1.8'。"""
    try:
        result = simple_eval(expression)
        return f"Result is: {result}"
    except Exception as e:
        return f"Error[calculation error]: {str(e)}"

@tool
def write_file(filename: str, content: str) -> str:
    """writes content into file, autocreation if undefined"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"write success: {filename}"
    except Exception as e:
        return f"write FAILED: {str(e)}"

@tool
def read_file(filename: str) -> str:
    """reads content from file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"read FAILED: {str(e)}"

# Integrated Tavily Search Tool
web_search = TavilySearchResults(
    max_results=3,
    description="Searches the web for up-to-date real-time facts, news, and external documentation."
)

tools = [calculate, write_file, read_file, web_search]

# 3. Initialize Deepseek LLM engin
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 4. Set memory Saver
memory = MemorySaver()

# 5. Set up standard ReAct Agent
agent = create_agent(llm, tools, checkpointer=memory)

# 6. Interactive interface
def main():
    print("=" * 60)
    print("Initializing agent......(based on DeepSeek and LangGraph)")
    print("Hint: Type in 'exit' or 'quit' to leave")
    print("=" * 60)
    
    # Session Thread ID
    config = {"configurable": {"thread_id": "session_001"}}
    
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Exiting system...")
                break
                
            print("\nthinking....\n")
            
            # process progress
            events = agent.stream(
                {"messages": [("user", user_input)]},
                config=config,
                stream_mode="values"
            )
            
            latest_message = None
            for event in events:
                latest_message = event["messages"][-1]
                
                if latest_message.type == "ai" and latest_message.tool_calls:
                    for tc in latest_message.tool_calls:
                        print(f"[Tool chose]: {tc['name']} | Para: {tc['args']}")
                elif latest_message.type == "tool":
                    print(f"[Tool return] {latest_message.name} Results:\n    {latest_message.content}")
            
            if latest_message and latest_message.content:
                print(f"\nAgent:\n{latest_message.content}")
                
        except Exception as e:
            print(f"\nERROR[runtime error]: {str(e)}")

if __name__ == "__main__":
    main()