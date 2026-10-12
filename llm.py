# LLM wrapper utilities
from langchain_anthropic import ChatAnthropic


def create_llm(model, max_tokens=1000):
    return ChatAnthropic(model=model, max_tokens=max_tokens)
