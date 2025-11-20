import os

from langchain_openai import ChatOpenAI


def must_new_openai_like() -> ChatOpenAI:
    """初始化 OpenAI-like LLM 模型"""
    llm = ChatOpenAI(
        model=os.environ["OPENAI_MODEL"],
        base_url=os.environ["OPENAI_API_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )
    return llm
