import os

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.agents import create_agent
import dotenv
from langchain_community.tools import DuckDuckGoSearchRun

class State(TypedDict):
    topic: str
    research_brief: str
    blog_post: str


def new_openai_like(**kwargs) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE_URL"],
        model=os.environ["OPENAI_MODEL"],
        **kwargs,
    )


def research(state: State):
    """
    Act as a senior research analyst
    """

    SYSTEM_PROMPT = (
        "You're an expert research analyst with advanced web research skills. "
        "You excel at finding, analyzing, and synthesizing information from "
        "across the internet using search tools. You're skilled at "
        "distinguishing reliable sources from unreliable ones, "
        "fact-checking, cross-referencing information, and "
        "identifying key patterns and insights. You provide "
        "well-organized research briefs with proper citations "
        "and source verification. Your analysis includes both "
        "raw data and interpreted insights, making complex "
        "information accessible and actionable."
    )

    # Senior Research Analyst
    analyst = create_agent(
        model=new_openai_like(),
        tools=[DuckDuckGoSearchRun()],
        system_prompt=SYSTEM_PROMPT,
        debug=True,
    )

    query = f"""1. Conduct comprehensive research on {state["topic"]} including:
                - Recent developments and news
                - Key industry trends and innovations
                - Expert opinions and analyses
                - Statistical data and market insights
            2. Evaluate source credibility and fact-check all information
            3. Organize findings into a structured research brief
            4. Include all relevant citations and sources


            Output a detailed research report containing:
            - Executive summary of key findings
            - Comprehensive analysis of current trends and developments
            - List of verified facts and statistics
            - All citations and links to original sources
            - Clear categorization of main themes and patterns
            Please format with clear sections and bullet points for easy reference."""

    r = analyst.invoke({"messages": [("user", query)]})

    return {"research_brief": r["messages"][-1].content}


def write_blog_post(state: State):
    """
    Act as a senior blog post writer
    """

    SYSTEM_PROMPT = (
        "You're a skilled content writer specialized in creating "
                "engaging, accessible content from technical research. "
                "You work closely with the Senior Research Analyst and excel at maintaining the perfect "
                "balance between informative and entertaining writing, "
                "while ensuring all facts and citations from the research "
                "are properly incorporated. You have a talent for making "
                "complex topics approachable without oversimplifying them."
    )

    writer = create_agent(
        model=new_openai_like(),
        system_prompt=SYSTEM_PROMPT,
        debug=True,
    )

    query = """Given the research brief wrapped within triple backticks as followed
        ```
        {state["research_brief"]}
        ```
    
        Using the research brief provided, create an engaging blog post that:
        1. Transforms technical information into accessible content
        2. Maintains all factual accuracy and citations from the research
        3. Includes:
            - Attention-grabbing introduction
            - Well-structured body sections with clear headings
            - Compelling conclusion
        4. Preserves all source citations in [Source: URL] format
        5. Includes a References section at the end"""

    # r = writer.invoke({"messages": [("user", query)]})    
    r = writer.invoke(query)
    return {"blog_post": r["messages"][-1].content}


def main():
    dotenv.load_dotenv()

    workflow = StateGraph(State)

    workflow.add_node("research", research)
    # workflow.add_node("write_blog_post", write_blog_post)

    workflow.add_edge(START, "research")
    # workflow.add_edge("research", "write_blog_post")
    # workflow.add_edge("write_blog_post", END)
    workflow.add_edge("research", END)

    chain = workflow.compile()

    state = chain.invoke({"topic": "AI trends in Dec. 10-18 of 2025"})
    print(f"research:\n{state['research_brief']}")
    # print(f'\n\nblog: {state["blog_post"]}')

if __name__ == "__main__":
    main()
