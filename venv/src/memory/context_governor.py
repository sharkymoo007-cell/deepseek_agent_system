from langchain_core.messages import SystemMessage, HumanMessage
from src.core.llm import llm_flash
from ..prompts import SUMMARIZER_PROMPT

class ContextGovernor:
    """Manages short-term context windows by dynamically summarizing large worker outputs."""

    @staticmethod
    def compress_observation(raw_output: str, max_length: int = 1600) -> str:
        """If observation exceeds max length, compress it using the LLM before returning to Manager."""
        if len(raw_output) <= max_length:
            return raw_output

        print(f"\n\033[33m[CONTEXT GOVERNOR]\033[0m Raw output length ({len(raw_output)} chars) exceeds threshold ({max_length}). Summarizing...")

        messages = [
            SystemMessage(content="You condense agent logs without losing core entities or data."),
            HumanMessage(content=SUMMARIZER_PROMPT.format(raw_output=raw_output))
        ]

        try:
            summary = llm_flash.invoke(messages).content
            return f"[SUMMARY OF SUB_AGENT OUTPUT]: {summary}"
        except Exception as e:
            # Fallback truncation if LLM summarization fails
            return raw_output[:max_length] + "\n...[TRUNCATED BY CONTEXT GOVERNOR]"

# Global singleton instance
context_governor = ContextGovernor()