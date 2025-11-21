import os

from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai_like import OpenAILikeEmbedding


def must_new_openai_like(model: str) -> OpenAILike:
    """初始化 OpenAI-like LLM 模型"""
    llm = OpenAILike(
        model=model,
        api_base=os.environ["OPENAI_API_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        is_chat_model=True,
        is_function_calling_model=True,
    )
    return llm


def must_new_openai_like_embedding(model: str) -> OpenAILikeEmbedding:
    """初始化 OpenAI-like LLM 模型"""
    embedding = OpenAILikeEmbedding(
        model_name=model,
        api_base=os.environ["OPENAI_API_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        embed_batch_size=10,
    )
    return embedding
