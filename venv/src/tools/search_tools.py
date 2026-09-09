from langchain_core.tools import tool
from langchain_tavily import TavilySearch

_tavily_search_internal = TavilySearch(max_results=3)

@tool
def web_search(query: str):
    """Searches the web for up-to-date information, news, real-time facts, and documentation."""
    try:
        return _tavily_search_internal.invoke({"query": query})
    except Exception as e:
        return f"Search FAILED: {str(e)}"