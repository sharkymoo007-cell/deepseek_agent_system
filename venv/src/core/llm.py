from langchain_openai import ChatOpenAI
from src.config import DEEPSEEK_API_KEY

llm_flash = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    reasoning_effort="high"
)

llm_pro = ChatOpenAI(
    model="deepseek-v4-pro",
    temperature=0,
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    reasoning_effort="max"
)