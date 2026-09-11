from src.core.main_agent import create_initial_plan, review_and_replan
from src.core.sub_agent import WORKER_MAP
from src.logger import AgentLogger
from src.memory.vector_store import memory_store
from src.memory.context_governor import context_governor

def run_multi_agent_pipeline(user_input: str, config: dict) -> str:
    # 1. main agent generate initial roadmap
    AgentLogger.log_header("MAIN: CREATING EXECUTION PLAN")
    plan = create_initial_plan(user_input)   # initialize Plan

    print(f"\033[35m[MANAGER PLAN INITIALIZED]\033[0m Goal: {plan.original_goal}")
    for st in plan.subtasks:
        print(f"├─ Task {st.task_id} [{st.assigned_Agent}]: {st.task_description}")

    step_count = 0
    max_step = 10

    while not plan.is_completed and step_count < max_step:
        step_count += 1
        current_subtask = plan.subtasks[plan.current_task_index]
        agent_name = current_subtask.assigned_Agent

        AgentLogger.log_header(f"STEP {step_count}: DISPATCHING TO [{agent_name.upper()}]")
        print(f"\033[33m[TASK EXECUTION]\033[0m: {current_subtask.task_description}")

        # 2. Dispatch subtask to corresponding worker agent
        worker_agent = WORKER_MAP.get(agent_name)
        if not worker_agent:
            last_output = f"Execution Error: Worker '{agent_name}' is not registered in WORKER_MAP."
        else:
            # Execute sub_agent loop
            response = worker_agent.invoke(
                {"messages": [("user", current_subtask.task_description)]},
                config=config
            )
            last_output = response["messages"][-1].content

            # Governance: Persist raw result to Long-Term Semantic VectorDB
            memory_store.save_task_memory(
                task_id=current_subtask.task_id,
                task_desc=current_subtask.task_description,
                worker=current_subtask.assigned_Agent,
                result=last_output
            )
            
            # Compress observation for Manager's Short-Term Context
            compressed_result = context_governor.compress_observation(last_output, max_length=600)

            AgentLogger.log_thought(f"Sub_agent Observation:\n{compressed_result}")

        # 3. Manager reviews worker output and dynamically replans trajectory
        AgentLogger.log_header(f"MAIN: REVIEWING TASK {current_subtask.task_id} RESULT")
        plan = review_and_replan(plan, last_output)
        
        if plan.is_completed:
            break

    if plan.final_summary:
        return plan.final_summary
    else:
        return "Task execution reached safety threshold without completion."