from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from src.core.llm import llm
from src.tools import all_tools
from src.prompts import SYSTEM_PROMPT
from src.logger import AgentLogger

memory = MemorySaver()

agent = create_agent(
    llm, 
    all_tools, 
    checkpointer=memory, 
    system_prompt=SYSTEM_PROMPT,
    interrupt_before=["tools"]
)

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
        last_msg = snapshot.values["messages"][-1]
        
        if last_msg.tool_calls:
            for tc in last_msg.tool_calls:
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