from src.logger import AgentLogger
from src.core.engine import run_multi_agent_pipeline

def main():
    print("=" * 60)
    print("Initializing agent......(based on DeepSeek and LangGraph)")
    print("Hint: Type in 'exit' or 'quit' to leave")
    print("=" * 60)
    
    config = {"configurable": {"thread_id": "session_001"}}
    
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q", "e"]:
                print("Goodbye! Exiting system...")
                break
            
            AgentLogger.log_header("AGENT INFERENCE START")
            final_resp = run_multi_agent_pipeline(user_input, config)
            AgentLogger.log_header("AGENT INFERENCE END")
            
            if final_resp:
                print(f"\n\033[1;35m[FINAL OUTPUT]:\033[0m\n{final_resp}")
                
        except Exception as e:
            print(f"\nERROR[runtime error]: {str(e)}")

if __name__ == "__main__":
    main()