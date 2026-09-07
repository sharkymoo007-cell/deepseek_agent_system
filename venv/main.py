import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from simpleeval import simple_eval
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langgraph.types import Command

load_dotenv()

# ====================Logging system======================

class AgentLogger:
    """Logs Agent Behavior and chain of thoughts"""

    @staticmethod
    def log_header(title: str):
        print(f"\n{'='*20} [{title}] {'='*20}")

    @staticmethod
    def log_thought(content: str):
        print(f"\033[36m[REASONING / CoT]:\033[0m\n{content}")

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

    @staticmethod
    def log_hitl_warning(tool_name: str, args: dict):
        print(f"\n\033[1;31m[HUMAN-IN-THE-LOOP INTERCEPTED]\033[0m")
        print(f"Agent requested high-risk operation:")
        print(f"  ├─ Target Action: {tool_name}")
        print(f"  └─ Proposed Args: {json.dumps(args, ensure_ascii=False)}")

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
    """writes content into file, autocreation if undefined, when naming a autocreated file, in addition to its name, add a time stamp and a agent signiture"""
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

@tool
def list_dir(path: str = ".") -> str:
    """Lists all files and directories in the specified local directory path. Default is current directory '.'"""
    try:
        files = os.listdir(path)
        if not files:
            return "Directory is empty."
        return "Files in directory:\n" + "\n".join([f"- {f}" for f in files])
    except Exception as e:
        return f"list_dir FAILED: {str(e)}"

@tool
def system_clock() -> str:
    """returns the current time from year to seconds of the system"""
    try:
        return f"The current system time in day/month/year, hour/minute/second is {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}"
    except Exception as e:
        return f"system_clock FAILED: {str(e)}"

tools = [calculate, write_file, read_file, web_search, list_dir, system_clock]

# 3. Initialize Deepseek LLM engin
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 4. Set memory Saver
memory = MemorySaver()

SYSTEM_PROMPT = """You are an advanced Autonomous AI Agent executing system tasks.

                [LANGUAGE REQUIREMENT]
                - You MUST reply and reason in the language the user is using.

                [EXECUTION PROTOCOL]
                For EVERY iteration, you MUST structure your thought process into the following sections BEFORE taking any action:

                1. <thought>: Analyze the current state, what information is missing, and what step to take next.
                2. <plan>: Outline the immediate next step (e.g., call a tool or present the final answer).

                [TOOL RULES]
                - For math operations, ALWAYS use 'calculate'.
                - Before writing files, read existing content if applicable.
                """
                            
# 5. Set up standard ReAct Agent
agent = create_agent(llm, 
                     tools, 
                     checkpointer=memory, 
                     system_prompt=SYSTEM_PROMPT,
                     interrupt_before=["tools"])

def run_agent_loop(payload, config):
    events = agent.stream(
        payload,
        config=config,
        stream_mode="updates"
    )
    
    step_count = 0
    final_response = ""

    for event in events:
        step_count += 1

        if not isinstance(event, dict):
            continue
        
        for node_name, node_update in event.items():

            if not isinstance(node_update, dict):
                continue

            messages = node_update.get("messages", [])
            for msg in messages:
                AgentLogger.log_state_delta(step_count, f"Node [{node_name}] -> {msg.__class__.__name__}")

                if msg.type == "ai":
                    if msg.content:
                        AgentLogger.log_thought(msg.content)
                        final_response = msg.content

                    if msg.tool_calls:
                        for tc in msg.tool_calls:
                            AgentLogger.log_tool_call(tc['name'], tc['args'], tc['id'])
                            
                elif msg.type == "tool":
                    AgentLogger.log_tool_result(msg.name, msg.content, msg.tool_call_id)

    snapshot = agent.get_state(config)
    
    if snapshot.next and "tools" in snapshot.next:
        # get next agent step
        last_msg = snapshot.values["messages"][-1]
        
        if last_msg.tool_calls:
            for tc in last_msg.tool_calls:
                # risk evaluation
                if tc["name"] == "write_file":
                    AgentLogger.log_hitl_warning(tc["name"], tc["args"])
                    
                    user_approval = input("\n[HUMAN INPUT REQUIRED] Approve operation? (y/n): ").strip().lower()
                    
                    if user_approval == 'y':
                        print("\033[32m[APPROVED] Executing operation...\033[0m")
                        return run_agent_loop(None, config)
                    else:
                        print("\033[31m[DENIED] Operation canceled by human. Feeding refusal back to Agent...\033[0m")
                        denial_message = {
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "name": tc["name"],
                            "content": "User Rejected Operation: Permission denied by human supervisor."
                        }
                        return run_agent_loop({"messages": [denial_message]}, config)
                else:
                    return run_agent_loop(None, config)

    return final_response

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
            final_resp = run_agent_loop({"messages": [("user", user_input)]}, config)
            
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
            if final_resp:
                print(f"\n\033[1;35m[FINAL OUTPUT]:\033[0m\n{final_resp}")
                
        except Exception as e:
            print(f"\nERROR[runtime error]: {str(e)}")

if __name__ == "__main__":
    main()