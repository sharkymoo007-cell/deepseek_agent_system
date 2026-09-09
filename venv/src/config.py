import os
import sys
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not DEEPSEEK_API_KEY:
    print("ERROR[not found]: Unable to find env var DEEPSEEK_API_KEY, please define!")
    sys.exit(1)

if not TAVILY_API_KEY:
    print("WARNING[not found]: TAVILY_API_KEY not found in environment. Web search may fail if called.")