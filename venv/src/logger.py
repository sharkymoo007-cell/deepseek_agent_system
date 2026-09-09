import json
from datetime import datetime

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