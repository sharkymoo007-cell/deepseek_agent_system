from langchain_core.tools import tool
from src.memory.vector_store import memory_store

@tool
def search_long_term_memory(query: str) -> str:
    """
    Search long-term memory for past execution results, saved files, or previous user tasks.
    Use this when you need information about what was generated or executed in past sessions.
    """
    memories = memory_store.query_relevant_memories(query, top_k=5)
    if not memories:
        return "No relevant past memories found."
    
    return "\n---\n".join(memories).join("\n---\n")