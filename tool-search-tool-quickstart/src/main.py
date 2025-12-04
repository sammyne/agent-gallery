import asyncio
import formatter
import logging
import os

from langchain.chat_models import BaseChatModel
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.tools import BaseTool, ToolRuntime, tool
from langchain_core.runnables.config import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.runtime import Runtime
from rank_bm25 import BM25Okapi
from typing_extensions import Literal

import github_mcp

logger = logging.getLogger(__name__)


class Toolkit:
    """工具集"""

    def __init__(self, tools: list[BaseTool], preloaded: list[BaseTool] | None = None):
        self.tools = dict([(t.name, t) for t in tools])
        self.descriptions = [f"{t.name} {t.description}" for t in tools]

        self.loaded = dict([(t.name, t) for t in preloaded]) if preloaded else dict()
        self.loaded_list = preloaded or []

        # Re-build index
        tokenized_corpus = [desc.lower().split(" ") for desc in self.descriptions]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def get(self, name: str) -> BaseTool:
        return self.loaded[name]

    def load(self, name: str):
        self.loaded[name] = self.tools[name]
        self.loaded_list.append(self.tools[name])

    def search(self, query: str, n: int = 3) -> list[str]:
        """根据名称获取功能可能满足要求的工具描述"""

        tokenized_query = query.lower().split(" ")
        top_docs = self.bm25.get_top_n(tokenized_query, self.descriptions, n=n)

        out = [doc.split("\n")[0][:120] for doc in top_docs]
        return out


class Context:
    def __init__(self, toolkit: Toolkit, model: BaseChatModel):
        self.toolkit = toolkit
        self.model = model


@tool
async def search_tools(query: str, runtime: ToolRuntime[Context]) -> list[str]:
    """Searches the external tool library for useful tools.

    Args:
        query: Keywords describing what you want to do (e.g., "github issues", "read file").
    """
    logger.info(f"[Agent Action] Searching for: '{query}'")

    return runtime.context.toolkit.search(query, n=5)


@tool
async def load_tool(name: str, runtime: ToolRuntime[Context]) -> str:
    """Loads a specific tool into your active toolkit.

    Args:
        name: The exact name of the tool to load (found via search_tools).
    """
    logger.info(f"[Agent Action] Loading tool: '{name}'")
    runtime.context.toolkit.load(name)

    return f"Tool '{name}' is now loaded and ready to use."


async def llm(state: MessagesState, runtime: Runtime[Context]):
    """LLM decides whether to call a tool or not"""

    tools = runtime.context.toolkit.loaded_list

    messages = state["messages"]
    model = runtime.context.model.bind_tools(tools)

    out = await model.ainvoke(messages)

    return {"messages": out}


async def toolkit(
    state: MessagesState, config: RunnableConfig, runtime: Runtime[Context]
):
    """Calls the requested tool and returns the result."""

    messages = []

    kit = runtime.context.toolkit

    tool_ctx = ToolRuntime(
        state=state,
        context=runtime.context,
        config=config,
        stream_writer=runtime.stream_writer,
        store=runtime.store,
        tool_call_id=None,
    )
    # https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolCall
    for v in state["messages"][-1].tool_calls:
        name = v["name"]
        tool_ctx.tool_call_id = v["id"]

        # 这个操作绕过 langgraph v1.0.5 的缺陷。
        # 详情参见 https://github.com/langchain-ai/langgraph/issues/6318
        args = v["args"] | {"runtime": tool_ctx}

        o = await kit.get(name).ainvoke(args)
        messages.append(ToolMessage(content=o, tool_call_id=v["id"]))

    return {"messages": messages}


def act_or_quit(state: MessagesState) -> Literal["toolkit", END]:
    """Decides whether to call a tool or finish the workflow."""

    if state["messages"][-1].tool_calls:
        return "toolkit"

    return END


def new_google_gemini() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=os.environ["GOOGLE_GEMINI_MODEL"],
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )


async def main():
    import dotenv

    dotenv.load_dotenv()

    FORMAT = "%(asctime)s - %(filename)s(%(lineno)d) - %(levelname)s: %(message)s"
    logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

    # Build workflow
    builder = StateGraph(MessagesState, context_schema=Context)

    # Add nodes
    builder.add_node("llm", llm)
    builder.add_node("toolkit", toolkit)

    # Add edges to connect nodes
    builder.add_edge(START, "llm")
    builder.add_conditional_edges("llm", act_or_quit, ["toolkit", END])
    # 添加工具调用完返回 LLM 节点的边
    builder.add_edge("toolkit", "llm")

    # Compile the agent
    agent = builder.compile()

    query = "Get details for issue https://github.com/SaschaHeyer/gen-ai-livestream/issues/6"

    kit = Toolkit(
        await github_mcp.new_client().get_tools(), preloaded=[search_tools, load_tool]
    )
    ctx = Context(toolkit=kit, model=new_google_gemini())

    input = {
        "messages": [
            SystemMessage(
                content='You are an agent. Your internal name is "GitHubManager".'
            ),
            HumanMessage(content=query),
        ]
    }

    r = await agent.ainvoke(input, context=ctx)
    print("\n=== Conversion History ===\n")
    for m in r["messages"]:
        if isinstance(m.content, str) or m.type == "tool":
            m.pretty_print()
            continue

        formatter.pretty_print_content_blocks(m.type, m.content_blocks)


if __name__ == "__main__":
    asyncio.run(main())
