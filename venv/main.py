import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from simpleeval import simple_eval
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

load_dotenv()

# ====================Logging system======================

class AgentLogger:
    """Logs Agent Behavior and chain of thoughts"""

    @staticmethod
    def log_header(title: str):
        print(f"\n{'='*20} [{title}] {'='*20}")

    @staticmethod
    def log_thought(content: str):
        print(f"\031[36m[REASONING / CoT]:\033[0m\n{content}")

    @staticmethod
    def log_tool_call(tool_name: str, args: dict, call_id: str):
        print(f"\033[33m[ACTION -> TOOL DISPATCH]:\033[0m")
        print(f"  ├─ Tool Name : {tool_name}")
        print(f"  ├─ Call ID   : {call_id}")
        print(f"  └─ Arguments : {json.dumps(args, ensure_ascii=False)}")

    @staticmethod
    def log_tool_result(tool_name: str, result: str, call_id: str):
        print(f"\033[32m[OBSERVATION <- ENVIRONMENT]:\033[0m")
        print(f"  ├─ Tool Name : {tool_name}")
        print(f"  ├─ Ref CallID: {call_id}")
        print(f"  └─ Payload   :\n{result}")

    @staticmethod
    def log_state_delta(step: int, msg_type: str):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\033[90m[TRACE {timestamp}] Step {step} | State Ingest: {msg_type}\033[0m")

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
_tavily_search_internal = TavilySearch(max_results=3)
@tool
def web_search(query: str):
    """Searches the web for up-to-date information, news, real-time facts, and documentation."""
    try:
        return _tavily_search_internal.invoke({"query": query})
    except Exception as e:
        return f"Search FAILED: {str(e)}"

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
            if user_input.lower() in ["exit", "quit", "q", "e"]:
                print("Goodbye! Exiting system...")
                break
            
            #print("\nthinking....\n")
            AgentLogger.log_header("AGENT INFERENCE LOOP START")

            # process progress
            events = agent.stream(
                {"messages": [("user", user_input)]},
                config=config,
                stream_mode="updates"
            )

            step_count = 0
            final_response = ""
            
            #latest_message = None
            for event in events:
                step_count += 1

                for node_name, node_update in event.items():
                    messages = node_update.get("messages", [])
                    for msg in messages:
                        AgentLogger.log_state_delta(step_count, f"Node [{node_name}] -> {msg.__class__.__name__}")

                        if msg.type == "ai":
                            if msg.content:
                                AgentLogger.log_thought(msg.content)
                                final_response = msg.content

                            if msg.tool_calls:
                                for tc in msg.tool_calls:
                                    AgentLogger.log_tool_call(
                                        tool_name=tc['name'],
                                        args=tc['args'],
                                        call_id=tc['id']
                                    )
                        elif msg.type == "tool":
                            AgentLogger.log_tool_result(
                                tool_name=msg.name,
                                result=msg.content,
                                call_id=msg.tool_call_id
                            )
            '''
                latest_message = event["messages"][-1]
                
                if latest_message.type == "ai" and latest_message.tool_calls:
                    for tc in latest_message.tool_calls:
                        print(f"[Tool chose]: {tc['name']} | Para: {tc['args']}")
                elif latest_message.type == "tool":
                    print(f"[Tool return] {latest_message.name} Results:\n    {latest_message.content}")
            
            if latest_message and latest_message.content:
                print(f"\nAgent:\n{latest_message.content}")
            '''
            AgentLogger.log_header("AGENT INFERENCE LOOP END")
            print(f"\n\033[1;35m[FINAL OUTPUT]:\033[0m\n{final_response}")
                
        except Exception as e:
            print(f"\nERROR[runtime error]: {str(e)}")

if __name__ == "__main__":
    main()