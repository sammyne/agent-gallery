import os
import re

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph


def new_openai_like_llm() -> ChatOpenAI:
    """初始化 OpenAI-like LLM 模型"""
    llm = ChatOpenAI(
        model=os.environ["OPENAI_MODEL"],
        base_url=os.environ["OPENAI_API_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0,
    )
    return llm


class AgentState(MessagesState):
    query: str
    code: str
    ok: str
    err: str


# Extract Python code from LLM response
class CodeExtractor(BaseOutputParser[str]):
    def parse(self, text: str) -> str:
        match = re.search(r"```python(.*?)```", text, re.DOTALL)
        return match.group(1).strip() if match else text.strip()


def generate(state: AgentState):
    llm = new_openai_like_llm()

    prompt_tmpl = ChatPromptTemplate.from_messages(
        [
            ("user", "Write Python code to do the following task:\n\n{query}"),
        ]
    )

    chain = prompt_tmpl | llm | CodeExtractor()
    out = chain.invoke({"query": state["query"]})
    # print(f'code goes as\n{out}\n\n')

    return {"code": out}


def execute(state: AgentState):
    GLOBALS = {
        "np": __import__("numpy"),
    }
    try:
        locals = {}
        exec(state["code"], GLOBALS, locals)
        out = locals.get("result", "No result variable set.")
        return {"ok": out}
    except Exception as e:
        return {"err": str(e)}


def main():
    import dotenv

    dotenv.load_dotenv()

    builder = StateGraph(AgentState)

    builder.add_node("generate", generate)
    builder.add_node("execute", execute)

    builder.add_edge(START, "generate")
    builder.add_edge("generate", "execute")
    builder.add_edge("execute", END)

    agent = builder.compile()

    query = "Plot a sine wave using matplotlib and numpy"

    r = agent.invoke({"query": query})
    print("\n=== Final Output ===")
    if "ok" in r:
        print(f"Ok:\n{r['ok']}")
        return

    print("Err:\n", r.get("err", "Unknown error"))


if __name__ == "__main__":
    main()
